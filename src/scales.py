from notes import Note


class Scale:
    def __init__(self):
        self.note_cnt = 0

    @staticmethod
    def type():
        return "Generic"


class HeptatonicScale(Scale):
    DIATONIC_INTERVALS = {
        "ionian":     "TTSTTTS",      # major
        "dorian":     "TSTTTST",
        "phrygian":   "STTTSTT",
        "lydian":     "TTTSTTS",
        "mixolydian": "TTSTTST",
        "aeolian":    "TSTTSTT",     # natural minor
        "locrian":    "STTSTTT"
    }

    def __init__(self, root_note: str, mode: str = "", octave=4):
        super().__init__()
        self.root = Note(name=root_note, octave=octave)
        if mode.lower() == "major" or mode == "":
            mode = "ionian"
        if mode.lower() == "minor":
            mode = "aeolian"
        self.mode = self._validate_mode(mode)
        self.notes = self._scale()
        self.note_cnt = 7

    @staticmethod
    def type():
        return "Heptatonic"

    def _scale(self):
        lst = list()
        lst.append(self.root)
        note = self.root
        for i in self.DIATONIC_INTERVALS[self.mode]:
            note = note + i
            lst.append(note)

        return lst

    def _validate_mode(self, mode):
        if mode.lower() in self.DIATONIC_INTERVALS.keys():
            return mode.lower()

        return None

    def __str__(self):
        ret = self.root.name() + " " + self.mode + ": "
        ret += " ".join([x.name() for x in self.notes])
        return ret


if __name__ == "__main__":
    scale = HeptatonicScale("C")
    print(scale)

    scale = HeptatonicScale("G")
    print(scale)

    scale = HeptatonicScale("C", "minor")
    print(scale)

    scale = HeptatonicScale("Cb")
    print(scale)

    scale = HeptatonicScale("Db", "dorian")
    print(scale)

    scale = HeptatonicScale("C#", "lydian")
    print(scale)

    for mode in HeptatonicScale.DIATONIC_INTERVALS.keys():
        scale = HeptatonicScale("G", mode)
        print(scale)
