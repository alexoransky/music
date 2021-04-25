from .notes import Note
from copy import deepcopy


class Scale:
    INTERVALS = {}

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
        if mode.lower() in self.INTERVALS.keys():
            return mode.lower()

        return None

    def __str__(self):
        return self.type()

    def name(self):
        return self.root.name() + " " + self.mode_name

    def note_names(self):
        return " ".join([x.name() for x in self.notes])


class HeptatonicScale(Scale):
    INTERVALS = {
        # diatonic scales
        "ionian":            "2212221",     # major
        "dorian":            "2122212",
        "phrygian":          "1222122",
        "lydian":            "2221221",
        "mixolydian":        "2212212",
        "aeolian":           "2122122",     # natural minor
        "locrian":           "1221222",

        "jazz minor":        "2122221",     # major with lowered 3rd
        "altered":           "1212222",     # altered dominant, palamidian, super-locrian, locrian with flat 4
        "phrygian dominant": "1312122",     # spanish gypsy, Hijaz - phrygian with risen 3rd
        "harmonic minor":    "2122131",     # natural minor with risen 7th
        "hungarian minor":   "2131131",     # gypsy minor
        "hungarian major":   "3121212",
        "ukranian dorian":   "2131212",
        "double harmonic":   "1312131"      # gypsy major
    }

    def __init__(self, root_note: str, mode: str = "", octave=4):
        super().__init__()
        self.root = Note(name=root_note, octave=octave)

        self.mode_name = mode
        self.notes = None

        _mode = mode
        if mode.lower() == "major" or mode == "":
            _mode = "ionian"
        if mode.lower() == "minor" or mode.lower() == "natural minor":
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
        for i in self.INTERVALS[self.mode]:
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
    INTERVALS = {
        "ionian":     "22323",       # major:                 heptatonic ioniam sans 4th and 7th degrees
        "dorian":     "23232",       # egyptian, suspended:   heptatonic dorian sans 3rd and 6th degrees
        "phrygian":   "32322",       # blues minor, Man Gong: heptatonic phrygian sans 2nd and 5th degrees
        "mixolydian": "23223",       # blues major, Ritsusen: heptatonic mixolydian sans 3rd and 7th degrees
        "aeolian":    "32232"        # natural minor:         heptatonic aeolian sans 2nd and 6th degrees
    }

    def __init__(self, root_note: str, mode: str = "", octave=4):
        super().__init__()
        self.root = Note(name=root_note, octave=octave)

        self.mode_name = mode

        _mode = mode
        if mode.lower() == "major" or mode == "":
            _mode = "ionian"
        if mode.lower() == "egyptian":
            _mode = "dorian"
        if mode.lower() == "blues minor":
            _mode = "phrygian"
        if mode.lower() == "blues major":
            _mode = "mixolydian"
        if mode.lower() == "natural minor":
            _mode = "aeolian"
        self.mode = self._validate_mode(_mode)

        extra_notes = None
        if self.mode == "ionian":
            extra_notes = (4, 7)
        if self.mode == "dorian":
            extra_notes = (3, 6)
        if self.mode == "phrygian":
            extra_notes = (2, 5)
        if self.mode == "mixolydian":
            extra_notes = (3, 7)
        if self.mode == "aeolian":
            extra_notes = (2, 6)

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


class HexatonicScale(Scale):
    INTERVALS = {
        "whole tone": "222222"
    }

    def __init__(self, root_note: str, octave=4):
        super().__init__()
        self.root = Note(name=root_note, octave=octave)

        self.mode = "whole tone"  # the only mode
        self.mode_name = self.mode
        self.notes = None

        self.notes = self._scale()
        self.note_cnt = 6

    @staticmethod
    def type():
        return "Hexatonic"

    def _scale(self):
        lst = list()
        lst.append(self.root)
        note = self.root
        for i in self.INTERVALS[self.mode]:
            note = note + i
            lst.append(note)

        return lst

    def __str__(self):
        ret = self.root.name() + " " + self.mode_name
        ret += ": "

        ret += " ".join([x.name() for x in self.notes])
        return ret
