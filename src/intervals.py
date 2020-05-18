import math
from num2words import num2words


class DiatonicInterval:
    SEMITONE_CNT = {"P1": 0,
                    "d2": 0,
                    "m2": 1,
                    "A1": 1,
                    "M2": 2,
                    "d3": 2,
                    "m3": 3,
                    "A2": 3,
                    "M3": 4,
                    "d4": 4,
                    "P4": 5,
                    "A3": 5,
                    "d5": 6,
                    "A4": 5,
                    "P5": 7,
                    "d6": 7,
                    "m6": 8,
                    "A5": 8,
                    "M6": 9,
                    "d7": 9,
                    "m7": 10,
                    "A6": 10,
                    "M7": 11,
                    "d8": 11,
                    "P8": 12,
                    "A7": 12,
                    "T": 2,
                    "S": 1}

    def __init__(self, name):
        """
        Creates a diatonic interval from the given name
        :param name: P1, m2, M2, P4, d3, A5 etc
        """
        self.name = None
        self.semitone_cnt = None
        self.pitch_ratio = None
        self.cent_cnt = None
        self.quality = None

        self.name = self._validate_name(name)
        if self.name is None:
            return

        self.semitone_cnt = self._semitone_cnt()
        self.pitch_ratio = self._pitch_ratio()
        self.cent_cnt = self._cent_cnt()
        self.quality = self._quality()

    def _validate_name(self, name):
        if name in self.SEMITONE_CNT.keys():
            return name
        return None

    def _semitone_cnt(self):
        return self.SEMITONE_CNT.get(self.name, None)

    def _pitch_ratio(self):
        return math.pow(2, self.semitone_cnt/12)

    def _cent_cnt(self):
        return self.semitone_cnt * 100

    def _quality(self):
        if self.name[0] == "m":
            return "minor"

        if self.name[0] == "M":
            return "major"

        if self.name[0] == "P":
            return "perfect"

        if self.name[0] == "d":
            return "diminished"

        if self.name[0] == "A":
            return "augmented"

        return ""

    def _number(self, short_ordinal=True):
        def ordinal(n):
            suffix = "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4]
            return f"{n}{suffix}"

        if len(self.name) == 1:
            if self.name == "T":
                return "tone"
            if self.name == "S":
                return "semitone"
            return ""

        num = int(self.name[1])
        if num == 1:
            return "unison"

        if num == 8:
            return "octave"

        if short_ordinal:
            return ordinal(num)

        return num2words(num, ordinal=True)

    def full_name(self, short_ordinal=True):
        return self._quality() + " " + self._number(short_ordinal)

    def degrees(self):
        if len(self.name) == 1:
            return 2

        return int(self.name[1])


if __name__ == "__main__":
    for name in DiatonicInterval.SEMITONE_CNT.keys():
        i = DiatonicInterval(name)
        print(f"{i.full_name()}: semitones: {i.semitone_cnt} pitch ratio: {i.pitch_ratio}")
