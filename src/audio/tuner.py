# the code below is inspired by Matt Zucker's ukulele tuner:
# https://mzucker.github.io/2016/08/07/ukulele-tuner.html

import numpy as np
from input_device import SDInputDevice, PAInputDevice
from transforms import STFT, CZT
from theory import Note
import time
from threading import Thread


class Tuner:
    INIT_TIME_S = 2
    DEBUG_OUTPUT = True

    THRESHOLD_DB = 25
    USE_SD = True
    USE_STFT = False
    if USE_STFT:
        SAMPLES_PER_FRAME = 2 * 1024
        FRAMES_PER_FFT = 16
    else:
        SAMPLES_PER_FRAME = 2 * 1024
        FREQ_STEP = 0.1

    def __init__(self, device, freq_range, samples_per_frame=SAMPLES_PER_FRAME, freq_step=FREQ_STEP):
        self.freq_range = freq_range
        self.threshold = Tuner.THRESHOLD_DB

        self.samples_per_frame = samples_per_frame

        if Tuner.USE_SD:
            self.device = SDInputDevice(device=device, samples_per_frame=self.samples_per_frame, queue_data=True)
        else:
            self.device = PAInputDevice(device=device, samples_per_frame=self.samples_per_frame, queue_data=True)

        self.sample_rate = self.device.get_sample_rate()

        if Tuner.USE_STFT:
            self.transform = STFT(self.sample_rate, samples_per_frame=self.samples_per_frame,
                                  frames_per_fft=Tuner.FRAMES_PER_FFT)
        else:
            self.transform = CZT(self.sample_rate, samples_per_frame=self.samples_per_frame, freq_range=freq_range,
                                 freq_step=freq_step)

        self.bin_range = (self.transform.freq_to_bin(self.freq_range[0]),
                          self.transform.freq_to_bin(self.freq_range[1]))

        self._active = False
        self._thread = None

    def start(self):
        if not self.device.data_is_queued():
            self.device.set_process_fn(self._process_data)
        self.device.start()
        self._active = True
        self._thread = Thread(target=self._main_loop)
        self._thread.start()

    def stop(self):
        self._active = False
        self.device.stop()
        self._thread.join()

    def _main_loop(self):
        def error_str():
            s = ""
            qsize = self.device.queue_size()
            qerrors = self.device.queue_error_cnt
            if qsize > 1:
                s = f"Q:{qsize} "
            if qerrors > 0:
                s = f"Q:{qsize} QE:{qerrors} "

            serrors = self.device.sample_error_cnt
            if serrors > 0:
                s += f"SE:{serrors}"

            if len(s):
                s = "[" + s.rstrip() + "]"
            return s

        nf = 0.0
        start_time = time.time()
        state = 0
        print("Sampling at {} Hz with max resolution of {:5.2f} Hz".format(self.transform.sample_rate,
                                                                           self.transform.freq_step))
        print("\rInitializing...", end="")

        while True:
            if not self._active:
                continue

            if state == 0:
                curr_time = time.time()
                if (curr_time - start_time) > Tuner.INIT_TIME_S:
                    if Tuner.DEBUG_OUTPUT:
                        print(f"\rNF={nf}             ")
                    print("\r                                        ", end="")
                    state = 1

            if self.device.data_is_queued():
                data = self.device.get_data()

            if state == 0:
                nf = self._determine_noise_floor(data, nf)

            if state == 1:
                peak_freq = self._process_data(data, nf)
                if peak_freq is None:
                    continue

                midi_num = Note.freq_to_midi_number(peak_freq)
                f0, _, _ = Note.midi_number_to_freq_hz(midi_num)
                note = Note.midi_number_to_note_name(midi_num)

                err_str = ""
                if Tuner.DEBUG_OUTPUT:
                    err_str = error_str()

                print("\r                                                  ", end="")
                print("\r{}  {:7.2f} Hz {:+.2f} Hz  {}".format(note, peak_freq, peak_freq - f0, err_str), end="")

    def _determine_noise_floor(self, data, nf):
        if data is None:
            return nf

        spectrum = self.transform.process(data)
        if spectrum is None:
            return nf

        clipped = spectrum[self.bin_range[0]:self.bin_range[1]]
        nf = max(nf, np.average(clipped))
        return nf

    def _process_data(self, data, nf=0):
        if data is None:
            return None

        spectrum = self.transform.process(data)
        if spectrum is None:
            return None

        clipped = spectrum[self.bin_range[0]:self.bin_range[1]]
        max_val = np.amax(clipped)

        if nf > 0:
            db = 20 * np.log10(max_val / nf)
            if db < self.threshold:
                return None
        else:
            if max_val < 0.01:
                return None

        peak_bin = clipped.argmax() + self.bin_range[0]
        peak_freq = self.transform.bin_to_freq(peak_bin)
        return peak_freq
