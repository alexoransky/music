# the code below is cleaned up and improved version of Matt Zucker's STFT:
# https://mzucker.github.io/2016/08/07/ukulele-tuner.html

import numpy as np


class STFT:
    def __init__(self, sample_rate, samples_per_frame=2048, frames_per_fft=16, sample_dtype=np.float32):
        """
        Creates an STFT transofm object
        The algorithm uses short time Fourier transform (STFT) in order to
        come up with averaged spectrum.  Using this approach, all samples that are
        generated within 1 second will be processed in small short-time frames.
        Refer to, for example,  Spectral Audio Signal Processing book for STFT theory:
        https://www.dsprelated.com/freebooks/sasp/

        Data is received one frame at a time and is processed in process() function

        The frame is assumed to have SAMPLES_PER_FRAME samples.
        Each frame is stored in buffer.
        The buffer can fit FRAMES_PER_FFT frames total.
        The total number of samples that can be stored in the buffer is SAMPLES_PER_FFT.
        SAMPLES_PER_FFT = SAMPLES_PER_FRAME * FRAMES_PER_FFT
        For instance, the FFT will be done over 16 frames and each frame has 2K samples.
        Therefore, the buffer has 32K samples.

        in the beginning, the buffer is filled with zeroes.
        Before a new frame is added, the FRAMES_PER_FFT-1 frames are shifted to the left
        (the beginning).
        The new frame is stored in the end (right side) of the buffer.

        The FFT is done over the entire windowed buffer (SAMPLES_PER_FFT samples) when a
        new frame is received.
        The window is Hann window function (raised cosine).

        :param sample_rate:       Sampling frequency in Hz
        :param samples_per_frame: How many samples per frame?
        :param frames_per_fft:    FFT takes average across how many frames?
        :param sample_dtype:      NumPy type of sample data
        """
        self.sample_rate = np.int32(sample_rate)              #
        self.samples_per_frame = np.int32(samples_per_frame)  #
        self.frames_per_fft = np.int32(frames_per_fft)        #
        self.sample_dtype = sample_dtype

        self.samples_per_fft = np.int32(self.samples_per_frame * self.frames_per_fft)
        self.freq_step = np.float32(self.sample_rate / self.samples_per_fft)

        # see discussion on Hann window function:
        # https://www.dsprelated.com/freebooks/sasp/Generalized_Hamming_Window_Family.html#eq:ghwf
        #
        # Matlab hann(n, 'perioldic') - creates zero only on the left endpoint, leaves the right for overlap
        # self.full_buffer_window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, self.samples_per_fft, False)))
        #
        # Matlab hann(n) - creates zeroes on both endpoints.
        self.full_buffer_window = np.hanning(self.samples_per_fft)

        self.buffer = None
        self.frame_cnt = 1
        self.clear()

    def clear(self):
        if self.frame_cnt < 1:
            return

        self.buffer = np.zeros(self.samples_per_fft, dtype=self.sample_dtype)
        self.frame_cnt = 0

    def update(self, data):
        # Shift the buffer down and new data in
        self.buffer[:-self.samples_per_frame] = self.buffer[self.samples_per_frame:]
        self.buffer[-self.samples_per_frame:] = np.frombuffer(data, self.sample_dtype)
        self.frame_cnt += 1

    def process(self, data):
        if data is None:
            self.clear()
            return None

        self.update(data)

        # Run the FFT on the windowed buffer
        window = self.full_buffer_window
        if self.frame_cnt < self.frames_per_fft:
            sample_cnt = self.frame_cnt*self.samples_per_frame
            window = np.hanning(sample_cnt)
            pad = np.zeros(self.samples_per_fft-sample_cnt, dtype=self.sample_dtype)
            window = np.append(window, pad)

        spectrum = np.abs(np.fft.rfft(self.buffer * window))

        return spectrum

    def bin_to_freq(self, bin):
        return bin * self.freq_step

    def freq_to_bin(self, freq):
        return np.int32(np.floor(freq / self.freq_step))
