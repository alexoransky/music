import math

class Tuning:
    def __init__(self, note_a_freq_hz=440):
        self.octave_offsets = [0.0] * 12
        self.pitch = [0.0] * 128
        for i in range(128):
            self.pitch[i] = i * 100.0

        self.note_a_freq_hz = note_a_freq_hz
        self.name = str(self.note_a_freq_hz) + " Hz 12-TET"
        if self.note_a_freq_hz == 440.0:
            return

        interval = 1200 * math.log2(self.note_a_freq_hz / 440.0)
        for i in range(12):
            self.octave_offsets[i] = interval
        for i in range(1, 128):
            self.pitch[i] += interval
