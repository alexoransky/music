# the code below is based on Matt Zucker's ukulele tuner:
# https://mzucker.github.io/2016/08/07/ukulele-tuner.html

import numpy as np
from input_device import SDInputDevice
from stft import STFT


DEVICE = 5
SAMPLE_RATE = 48000
SAMPLES_PER_FRAME = 2048
FRAMES_PER_FFT = 16

NOTE_MIN = 60       # C4
NOTE_MAX = 69       # A4
NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()


class Tuner:
    def __init__(self):
        self.samples_per_frame = SAMPLES_PER_FRAME
        self.frames_per_fft = FRAMES_PER_FFT

        self.device = SDInputDevice(device=DEVICE, samples_per_frame=self.samples_per_frame, queue_data=False)
        self.sample_rate = self.device.get_sample_rate()
        self.stft = STFT(self.sample_rate, samples_per_frame=self.samples_per_frame, frames_per_fft=self.frames_per_fft)
        self.device.set_process_fn(self.process)

        self.num_frames = 0
        self.samples_per_fft = np.int32(self.samples_per_frame * self.frames_per_fft)
        self.freq_step = np.float32(self.sample_rate / self.samples_per_fft)

        self.imin = max(0, int(np.floor(self.note_to_fftbin(NOTE_MIN - 1))))
        self.imax = min(self.samples_per_fft, int(np.ceil(self.note_to_fftbin(NOTE_MAX + 1))))

        print(f"Sampling at {self.stft.sample_rate} Hz with max resolution of {self.stft.freq_step} Hz")
        print()

        self.device.start()

    def freq_to_number(self, f):
        return 69 + 12 * np.log2(f / 440.0)

    def number_to_freq(self, n):
        return 440 * 2.0 ** ((n - 69) / 12.0)

    def note_name(self, n):
        return NOTE_NAMES[n % 12]

    def note_to_fftbin(self, n):
        return self.number_to_freq(n) / self.freq_step

    def process(self, data):
        spectrum = self.stft.process(data)

        if spectrum is None:
            print("\r                                        ", end="")
            return

        # max_val = np.amax(spectrum[self.imin:self.imax])
        # min_val = np.amin(spectrum)

        # Get frequency of maximum response in range
        freq = (spectrum[self.imin:self.imax].argmax() + self.imin) * self.freq_step

        # Get note number and nearest note
        n = self.freq_to_number(freq)
        n0 = int(round(n))

        # Console output once we have a full buffer
        self.num_frames += 1

        if self.num_frames >= self.frames_per_fft:
            print("\r                                        ", end="")
            print("\r{}  {:7.2f} Hz {:+.2f}".format(self.note_name(n0), freq, n - n0), end="")


if __name__ == "__main__":
    print(SDInputDevice.available_devices())

    tuner = Tuner()
