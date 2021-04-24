# the code below is inspired by Matt Zucker's ukulele tuner:
# https://mzucker.github.io/2016/08/07/ukulele-tuner.html

import numpy as np
from audio.input_device import SDInputDevice, PAInputDevice
from audio.transforms import STFT, CZT
from theory import Note
import time
from threading import Thread
from dataclasses import dataclass
from typing import Tuple


@dataclass
class TunerData:
    samples: object = None
    noise_floor: int = 0
    midi_num: int = 0
    note: str = ""
    curr_freq: float = 0.0
    delta_freq: float = 0.0
    state: int = 0
    queue_size: int = 0


@dataclass
class TunerErrors:
    queue: int = 0
    sample: int = 0


class Tuner:
    INIT_STATE = 0
    PROCESS_STATE = 1

    INIT_TIME_S = 2
    THRESHOLD_DB = 25
    USE_SD = True
    USE_STFT = False

    if USE_STFT:
        SAMPLES_PER_FRAME = 2 * 1024
        FRAMES_PER_FFT = 16
        FREQ_STEP = 1.0
    else:  # CZT
        SAMPLES_PER_FRAME = 2 * 1024
        FREQ_STEP = 0.1

    def __init__(self, device: int, note_range: Tuple[str, str],
                 samples_per_frame: int = SAMPLES_PER_FRAME, freq_step: float = FREQ_STEP,
                 note_a_freq_hz: float = 440.0):

        self.freq_range = Tuner.get_freq_range(note_range, note_a_freq_hz)
        self.threshold = Tuner.THRESHOLD_DB
        self.note_a_freq_hz = note_a_freq_hz

        self.samples_per_frame = samples_per_frame

        self.device = None
        if Tuner.USE_SD:
            self.device = SDInputDevice(device=device, samples_per_frame=self.samples_per_frame, queue_data=True)
        else:
            self.device = PAInputDevice(device=device, samples_per_frame=self.samples_per_frame, queue_data=True)

        self.sample_rate = self.device.get_sample_rate()

        if Tuner.USE_STFT:
            self.transform = STFT(self.sample_rate, samples_per_frame=self.samples_per_frame,
                                  frames_per_fft=Tuner.FRAMES_PER_FFT)
        else:
            self.transform = CZT(self.sample_rate, samples_per_frame=self.samples_per_frame, freq_range=self.freq_range,
                                 freq_step=freq_step)

        self.bin_range = (self.transform.freq_to_bin(self.freq_range[0]),
                          self.transform.freq_to_bin(self.freq_range[1]))

        self._active = False
        self._thread = None

        self.data = TunerData()
        self.errors = TunerErrors()

    @classmethod
    def get_freq_range(cls, note_range, note_a_freq_hz):
        f1 = Note.note_name_to_freq_hz(note_range[0], note_a_freq_hz=note_a_freq_hz)
        f2 = Note.note_name_to_freq_hz(note_range[1], note_a_freq_hz=note_a_freq_hz)
        return f1[0], f2[0]

    def start(self):
        if self.device is None:
            return

        # only start if data will be queued
        if not self.device.data_is_queued():
            return

        self.data.state = Tuner.INIT_STATE
        self.device.start()
        self._active = True
        self._thread = Thread(target=self._main_loop)
        self._thread.start()

    def stop(self):
        self._active = False
        self.device.stop()
        self._thread.join()

    def _main_loop(self):
        start_time = time.time()

        while True:
            if not self._active:
                continue

            if self.data.state == Tuner.INIT_STATE:
                curr_time = time.time()
                if (curr_time - start_time) > Tuner.INIT_TIME_S:
                    self.data.state = Tuner.PROCESS_STATE
                    self.on_state_change()
                    continue

            self.data.samples = self.device.get_data()

            if self.data.state == Tuner.INIT_STATE:
                self._determine_noise_floor(self.data.samples)
                continue

            if self.data.state == Tuner.PROCESS_STATE:
                peak_freq = self._get_peak_freq(self.data.samples)
                if peak_freq is None:
                    continue

                midi_num = Note.freq_to_midi_number(peak_freq, note_a_freq_hz=self.note_a_freq_hz)
                f0, _, _ = Note.midi_number_to_freq_hz(midi_num, note_a_freq_hz=self.note_a_freq_hz)
                note = Note.midi_number_to_note_name(midi_num)

                self.data.queue_size = self.device.queue_size()
                self.errors.queue = self.device.queue_error_cnt
                self.errors.sample = self.device.sample_error_cnt

                self.data.note = note
                self.data.midi_num = midi_num
                self.data.curr_freq = peak_freq
                self.data.delta_freq = peak_freq - f0

            self.on_update()

    def _determine_noise_floor(self, data):
        if data is None:
            return

        spectrum = self.transform.process(data)
        if spectrum is None:
            return

        clipped = spectrum[self.bin_range[0]:self.bin_range[1]]
        self.data.noise_floor = max(self.data.noise_floor, np.average(clipped))

    def _get_peak_freq(self, data):
        if data is None:
            return None

        spectrum = self.transform.process(data)
        if spectrum is None:
            return None

        clipped = spectrum[self.bin_range[0]:self.bin_range[1]]
        max_val = np.amax(clipped)

        if self.data.noise_floor > 0:
            db = 20 * np.log10(max_val / self.data.noise_floor)
            if db < self.threshold:
                return None
        else:
            if max_val < 0.01:
                return None

        peak_bin = clipped.argmax() + self.bin_range[0]
        peak_freq = self.transform.bin_to_freq(peak_bin)
        return peak_freq

    def on_state_change(self):
        pass

    def on_update(self):
        pass
