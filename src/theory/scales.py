from .notes import Note
from copy import deepcopy


class Scale:
    DIATONIC_INTERVALS = {}

    def __init__(self):
        self.note_cnt = 0
        self.root = None
        self.notes = None
        self.mode = ""
        self.mode_name = ""

    @staticmethod
    def type():
        return "Generic"

    def _validate_mode(self, mode):
        if mode.lower() in self.DIATONIC_INTERVALS.keys():
            return mode.lower()

        return None

    def __str__(self):
        return self.type()


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

        self.mode_name = mode
        self.notes = None

        _mode = mode
        if mode.lower() == "major" or mode == "":
            _mode = "ionian"
        if mode.lower() == "minor":
            _mode = "aeolian"
        self.mode = self._validate_mode(_mode)
        if self.mode is None:
            self.mode_name = "unknown"
            return

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

    def __str__(self):
        ret = self.root.name() + " " + self.mode_name
        if self.mode_name != self.mode:
            ret += f" ({self.mode})"
        ret += ": "

        ret += " ".join([x.name() for x in self.notes])
        return ret


class PentatonicScale(Scale):
    DIATONIC_INTERVALS = {
        "ionian":     "TT3T3",       # major:                 heptatonic ioniam sans 4th and 7th degrees
        "dorian":     "T3T3T",       # egyptian, suspended:   heptatonic dorian sans 3rd and 6th degrees
        "phrygian":   "3T3TT",       # blues minor, Man Gong: heptatonic phrygian sans 2nd and 5th degrees
        "mixolydian": "T3TT3",       # blues major, Ritsusen: heptatonic mixolydian sans 3rd and 7th degrees
        "aeolian":    "3TT3T"        # natural minor:         heptatonic aeolian sans 2nd and 6th degrees
    }

    def __init__(self, root_note: str, mode: str = "", octave=4):
        super().__init__()
        self.root = Note(name=root_note, octave=octave)

        self.mode_name = mode

        _mode = mode
        if mode.lower() == "major" or mode == "":
            _mode = "ionian"
            extra_notes = (4, 7)
        if mode.lower() == "egyptian":
            _mode = "dorian"
            extra_notes = (3, 6)
        if mode.lower() == "blues minor":
            _mode = "phrygian"
            extra_notes = (2, 5)
        if mode.lower() == "blues major":
            _mode = "mixolydian"
            extra_notes = (3, 7)
        if mode.lower() == "natural minor":
            _mode = "aeolian"
            extra_notes = (2, 6)
        self.mode = self._validate_mode(_mode)
        if self.mode is None:
            self.mode_name = "unknown"
            return

        # TODO: this is a hack, need to figure out how to generate scales
        #       without using diatonic intervals
        # in order to generate a scale with correct note names,
        # first construct a heptatonic scale and then delete extra notes
        hept_scale = HeptatonicScale(root_note, _mode)
        self.notes = deepcopy(hept_scale.notes)
        del self.notes[extra_notes[1]-1]
        del self.notes[extra_notes[0]-1]

        self.note_cnt = 5

    @staticmethod
    def type():
        return "Pentatonic"

    def __str__(self):
        ret = self.root.name() + " " + self.mode_name
        if self.mode_name != self.mode:
            ret += f" ({self.mode})"
        ret += " " + self.type().lower()
        ret += ": "

        ret += " ".join([x.name() for x in self.notes])
        return ret
