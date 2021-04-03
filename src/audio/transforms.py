# the STFT code below is a cleaned up and improved version of Matt Zucker's STFT:
# https://mzucker.github.io/2016/08/07/ukulele-tuner.html

# the CZT code below is based on Garrett J's code for the CZT transform:
# https://github.com/garrettj403/CZT/blob/main/czt.py
# The code was cleaned up and optimized for speed (2x gain).
# For the algorithm white paper, refer to
# Sukhoy, V., Stoytchev, A. Generalizing the inverse FFT off the unit circle. Sci Rep 9, 14443 (2019).
# https://doi.org/10.1038/s41598-019-50234-9

import numpy as np
import math
from copy import copy
from typing import Tuple
from abc import ABC, abstractmethod

fft = np.fft.fft
rfft = np.fft.rfft
ifft = np.fft.ifft


class Transform(ABC):
    @abstractmethod
    def process(self, data: np.array) -> np.array:
        return None

    @abstractmethod
    def bin_to_freq(self, bin: int) -> float:
        return 0.0

    @abstractmethod
    def freq_to_bin(self, freq: float) -> int:
        return 0


class STFT(Transform):
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
        self.sample_rate = np.int32(sample_rate)
        self.samples_per_frame = np.int32(samples_per_frame)
        self.frames_per_fft = np.int32(frames_per_fft)
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
        self.window = []
        pad = np.zeros(self.samples_per_fft, dtype=self.sample_dtype)
        self.window.append(pad)  # window[0] is all zeroes
        for i in range(1, self.frames_per_fft+1):
            sample_cnt = i*self.samples_per_frame
            window = np.hanning(sample_cnt)
            if sample_cnt < self.samples_per_fft:
                pad = np.zeros(self.samples_per_fft-sample_cnt, dtype=self.sample_dtype)
                window = np.append(window, pad)
            self.window.append(window)

        self.buffer = None
        self.frame_cnt = 1
        self._clear()

    def _clear(self):
        if self.frame_cnt < 1:
            return

        self.buffer = np.zeros(self.samples_per_fft, dtype=self.sample_dtype)
        self.frame_cnt = 0

    def _update(self, data):
        # Shift the buffer down and new data in
        self.buffer[:-self.samples_per_frame] = self.buffer[self.samples_per_frame:]
        self.buffer[-self.samples_per_frame:] = np.frombuffer(data, self.sample_dtype)
        self.frame_cnt += 1

    def process(self, data):
        if data is None:
            self._clear()
            return None

        self._update(data)

        # Run the FFT on the windowed buffer
        window = self.window[min(self.frames_per_fft, self.frame_cnt)]
        return np.abs(rfft(self.buffer * window))

    def bin_to_freq(self, bin):
        return bin * self.freq_step

    def freq_to_bin(self, freq):
        return np.int32(np.floor(freq / self.freq_step))


class CZT(Transform):
    def __init__(self, sample_rate: int, samples_per_frame: int, freq_range: Tuple[float, float], freq_step: float,
                 sample_dtype=np.float32):
        """
        The class implements the Chirp Z transform.
        The class works on samples that delivered in a frame.
        The frequency range should be a lot narrower than the Nyquist frequency for the CZT to work fast.
        :param sample_rate: sampling frequency, e.g. 48000
        :param samples_per_frame:number of samples per frame, e.g. 2048
        :param freq_range: a tuple of (min_freq, max_freq), Hz, e.g. (65, 250)
        :param freq_step: Desired resolution, Hz, e.g. 0.1
        :param sample_dtype: The NumPy type for the sample, e.g. np.float32
        """
        self.sample_rate = np.int32(sample_rate)
        self.samples_per_frame = np.int32(samples_per_frame)
        self.freq_range = freq_range
        self.freq_step = np.float32(freq_step)
        self.sample_dtype = sample_dtype
        self.frame_cnt = 0

        # precompute values for CZT
        Fs = self.sample_rate
        f = np.arange(self.freq_range[0], self.freq_range[1], self.freq_step)
        f1, f2 = f.min(), f.max()
        bw = f2 - f1  # bandwidth
        self.k = Fs / bw   # correction factor (normalization)
        self.Nf = len(f)                                        # number of frequency points
        self.W = np.exp(-2j * np.pi * bw / (self.Nf - 1) / Fs)  # step
        self.A = np.exp(2j * np.pi * f1 / Fs)                   # starting point

        self.N = np.arange(self.samples_per_frame)
        self.M = np.arange(self.Nf)
        self.WA = self.W ** (self.N ** 2 / 2) * self.A ** -self.N

        # first row and first column of Toeplitz matrix
        self.r = self.W ** (-(self.N ** 2) / 2)
        self.c = self.W ** (-(self.M ** 2) / 2)

        N = len(self.r)
        M = len(self.c)
        self.n = int(2 ** np.ceil(np.log2(M + N - 1)))

        # first column of circulant matrix G
        self.chat = np.r_[self.c, np.zeros(self.n - (M + N - 1)), self.r[-(N - 1):][::-1]]
        self.C = fft(self.chat)

    def _toeplitz_mult_ce(self, x):
        """
        Multiply Toeplitz matrix by vector using circulant embedding.
        "Compute the product y = Tx of a Toeplitz matrix T and a vector x, where T
        is specified by its first row r = (r[0], r[1], r[2],...,r[N-1]) and its
        first column c = (c[0], c[1], c[2],...,c[M-1]), where r[0] = c[0]."
        See algorithm S1 in Sukhoy & Stoytchev 2019.
        :param x: (np.ndarray): vector to multiply the Toeplitz matrix
        :return: np.ndarray: product of Toeplitz matrix and vector x
        """
        # zero-pad x
        m = len(x)
        xhat = np.zeros(self.n, dtype=complex)
        xhat[:m] = x

        yhat = self._circulant_multiply(xhat)
        y = yhat[:len(self.c)]
        return y

    def _circulant_multiply(self, x):
        """
        Multiply a circulant matrix by a vector.
        Compute the product y = Gx of a circulant matrix G and a vector x, where G
        is generated by its first column c=(c[0], c[1],...,c[n-1]).
        Runs in O(n log n) time.
        See algorithm S4 in Sukhoy & Stoytchev 2019.
        :param x: (np.ndarray): vector x
        :return: np.ndarray: product Gx
        """
        n = len(self.chat)

        X = fft(x)

        Y = np.empty(n, dtype=complex)
        for k in range(n):
            Y[k] = self.C[k] * X[k]

        y = ifft(Y)
        return y

    def czt(self, x):
        X = self._toeplitz_mult_ce(self.WA * x)

        for k in range(self.Nf):
            X[k] = self.W ** (k ** 2 / 2) * X[k]

        return X

    def process(self, data):
        if data is None:
            return None

        self.frame_cnt += 1
        buffer = copy(np.frombuffer(data, self.sample_dtype))
        freq_data = self.czt(buffer)
        return np.abs(freq_data)

    def bin_to_freq(self, bin):
        return bin * self.freq_step + self.freq_range[0]

    def freq_to_bin(self, freq):
        return np.int32(np.floor((freq-self.freq_range[0]) / self.freq_step))
