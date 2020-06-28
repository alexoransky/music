import math


class Tuning:
    TUNING_12_TET = 0
    TUNING_5_LIMIT = 1

    def __init__(self, note_a_freq_hz=440, tuning=TUNING_12_TET):
        # offesets in cents with an octave
        self.offsets = [0.0] * 12

        # pitch values in cents from note 0 to note 127
        # in 12-TET each note is 100 cents higher than the previous
        self.pitch = [0.0] * 128
        for i in range(128):
            self.pitch[i] = i * 100.0

        self.note_a_freq_hz = note_a_freq_hz
        self.tuning = tuning
        self.name = str(self.note_a_freq_hz) + " Hz 12-TET"
        if self.note_a_freq_hz == 440.0:
            return

        interval = 1200 * math.log2(self.note_a_freq_hz / 440.0)
        for i in range(12):
            self.offsets[i] = interval
        for i in range(1, 128):
            self.pitch[i] += interval

        if tuning == self.TUNING_5_LIMIT:
            intervals = self.intervals_5_limit()
            for i in range(12):
                self.offsets[i] += (intervals[i] - 100*i)


    def intervals_5_limit(self, num=0):
        """
        See the method to build 12 tone scales for 5-limit tuningL
        https://en.wikipedia.org/wiki/Five-limit_tuning
        :param num: 0, 1 or 2
        :return:list of 12 intervals
        """
        scale = []
        scale.append([5/3, 5/4, 15/8, 45/32, 16/9, 4/3, 1, 3/2, 9/8, 16/15, 8/5, 6/5])
        scale.append([10/9, 5/3, 5/4, 15/8, 45/32, 4/3, 1, 3/2, 16/15, 8/5, 6/5, 9/5])
        scale.append([5/3, 5/4, 15/8, 45/32, 4/3, 1, 3/2, 9/8, 16/15, 8/5, 6/5, 9/5])

        intervals = [1200*math.log2(i) for i in scale[num]]
        intervals.sort()
        from pprint import pprint
        pprint(intervals)
        return intervals
