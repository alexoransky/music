from .notes import Note


class Scale:
    TYPE = "Generic"
    NOTES_CNT = 0
    INTERVALS = {}   # maps mode to intervals string
    SCALE_NAME = {}  # maps mode to scale name

    def __init__(self, root_note: str, mode: str = "", octave: int = 4):
        self._root_note = root_note
        self._mode = mode
        self._octave = octave

        self.root = Note(name=root_note, octave=octave)
        self.mode = self._validate_mode(mode)

        self.notes = None
        if self.mode is None:
            return

        self.notes = self._scale()
        self._normalize()

    def _validate_mode(self, mode: str) -> str:
        """
        The method validates the supplied mode against the modes specified in INTERVALS dict.
        Overwrite this method to map other mode names to the specified ones.
        :param mode: Mode name, e.g. "minor"
        :return: mode know from INTERVALS or None if not found
        """
        if mode.lower() in self.INTERVALS.keys():
            return mode.lower()

        return None

    def _mode_name(self) -> str:
        """
        The method creates the mode name from self.mode
        :return: Mode name or "unknown"
        """
        if self.mode is None:
            return "unknown"

        return self.mode

    def _scale(self) -> list[Note]:
        """
        The method builds the scale from the root note and the scale intervals, given by the mode
        :return: list of notes that belong to the scale
        """
        lst = list()
        lst.append(self.root)
        note = self.root
        for i in self.INTERVALS[self.mode][:-1]:
            note = note + i
            lst.append(note)

        return lst

    def _normalize(self):
        """
        The method is intended to resolve note names to names that are accpetable in the scale,
        e.g. Cb can be changed to B etc. The method works on self.notes.
        If normalization fails, the note list should be left intact.
        :return: True if normalization was successful, False, otherwise.
        """
        return True

    def __repr__(self):
        return f"{type(self).__name__}({self._root_note}, {self._mode}, {self._octave})"

    def __str__(self):
        ret = f"{self.root.name()}  {self.mode_name()}: "
        ret += " ".join([x.name() for x in self.notes])
        return ret

    def name(self) -> str:
        """
        The method returns the scale name
        :return: Scale name, including the mode name, e.g. "C minor pentatonic"
        """
        scale_name = self.SCALE_NAME.get(self.mode, self.mode)
        if scale_name is None:
            scale_name = "unknown"
        return f"{self.root.name()} {scale_name}"

    def mode_name(self) -> str:
        """
        The method returns the mode name of the scale
        :return: Mode name, e.g. "aeolian"
        """
        if self.mode is None:
            return "unknown"
        return self.mode

    def note_names(self) -> str:
        """
        The method returns the scale notes
        :return: Scale notes, e.g. "E F G♯ A B C D E"
        """
        if self.notes is None or len(self.notes) == 0:
            return ""

        return " ".join([x.name() for x in self.notes])

    @staticmethod
    def next_note(note):
        notes = ["A", "B", "C", "D", "E", "F", "G"]
        idx = Note.NOTES[note]
        if idx + 1 >= len(notes):
            return "A"
        return notes[idx + 1]

    @staticmethod
    def match_note(note: str, note_names: tuple):
        # note is the name without any accidental
        # note names can be with accidentals
        for name in note_names:
            if name[0] == note:
                return True
        return False


class PentatonicScale(Scale):
    TYPE = "Pentatonic"
    NOTES_CNT = 5
    INTERVALS = {
        "ionian":     "22323",       # major:                     heptatonic ionian sans 4th and 7th degrees
        "dorian":     "23232",       # egyptian, suspended:       heptatonic dorian sans 3rd and 6th degrees
        "phrygian":   "32322",       # blues minor, Man Gong:     heptatonic phrygian sans 2nd and 5th degrees
        "mixolydian": "23223",       # blues major, Ritsusen, yo: heptatonic mixolydian sans 3rd and 7th degrees
        "aeolian":    "32232",       # natural minor:             heptatonic aeolian sans 2nd and 6th degrees
        # TODO add japanese scales  https://www.musicnotes.com/now/musictheory/japanese-scales-in-music-theory
        # "in":         "14221"        # sakura pentatonic
    }
    # TODO add prygian dominant pentatonic

    SCALE_NAME = {
        "ionian":     "major pentatonic",
        "dorian":     "egyptian (suspended)",
        "phrygian":   "blues minor",
        "mixolydian": "blues major",
        "aeolian":    "minor pentatonic",
    }

    def _validate_mode(self, mode):
        _mode = mode
        if mode.lower() == "major" or mode == "":
            _mode = "ionian"
        if mode.lower() == "egyptian":
            _mode = "dorian"
        if mode.lower() == "blues minor":
            _mode = "phrygian"
        if mode.lower() == "blues major" or mode == "yo":
            _mode = "mixolydian"
        if mode.lower() == "minor" or mode.lower() == "natural minor":
            _mode = "aeolian"

        return super()._validate_mode(_mode)

    def __str__(self):
        ret = f"{self.root.name()}  {self.TYPE.lower()} {self.mode_name()}: "
        ret += " ".join([x.name() for x in self.notes])
        return ret

    def _normalize(self):
        skipped_degrees = {
            "ionian":     (4, 7),
            "dorian":     (3, 6),
            "phrygian":   (2, 5),
            "mixolydian": (3, 7),
            "aeolian":    (2, 6)
            # "in":         (1, None)
        }

        if len(self.notes) == 0:
            return True

        normalized = self.notes.copy()

        next_expected = normalized[0].name()[0]
        note_idx = 0
        for deg_idx in range(1, 8):
            if deg_idx in skipped_degrees[self.mode]:
                next_expected = self.next_note(next_expected)
                continue

            n = normalized[note_idx]
            if n.name()[0] != next_expected:
                if not self.match_note(next_expected, n.names):
                    return False
                n.use_other_name(next_expected)
            next_expected = self.next_note(next_expected)
            note_idx += 1
            if note_idx >= self.NOTES_CNT:
                break

        self.notes = normalized
        return True


class HexatonicScale(Scale):
    TYPE = "Hexatonic"
    NOTES_CNT = 6
    INTERVALS = {
        "whole tone": "222222",
        "major":      "221223",
        "minor":      "212232",
        "augmented":  "313131",
        "blues":      "311232"
    }

    SCALE_NAME = {
        "major": "major hexatonic",
        "minor": "minor hexatonic"
    }

    def _normalize(self):
        skipped_degrees = {
            "major": (7, ),
            "minor": (6, ),
        }

        if len(self.notes) == 0:
            return True

        if self.mode == "blues":
            pentatonic = PentatonicScale(self._root_note, "minor", self._octave)
            self.notes = pentatonic.notes.copy()
            blue_note = Note(self.notes[0].name()) + 6
            blue_note.use_other_name(suggested_root=self.notes[3].name()[0])
            self.notes.insert(3, blue_note)
            return True

        normalized = self.notes.copy()

        next_expected = normalized[0].name()[0]
        note_idx = 0
        for deg_idx in range(1, 8):
            if deg_idx in skipped_degrees.get(self.mode, (0, )):
                next_expected = self.next_note(next_expected)
                continue

            n = normalized[note_idx]
            if n.name()[0] != next_expected:
                if not self.match_note(next_expected, n.names):
                    return False
                n.use_other_name(next_expected)
            next_expected = self.next_note(next_expected)
            note_idx += 1
            if note_idx >= self.NOTES_CNT:
                break

        self.notes = normalized
        return True


class HeptatonicScale(Scale):
    TYPE = "Heptatonic"
    NOTES_CNT = 7
    INTERVALS = {
        # diatonic scales
        "ionian":            "2212221",     # major
        "dorian":            "2122212",
        "phrygian":          "1222122",
        "lydian":            "2221221",
        "mixolydian":        "2212212",
        "aeolian":           "2122122",     # natural minor
        "locrian":           "1221222",

        "major locrian":     "2211222",     # locrian major
        "jazz minor":        "2122221",     # major with lowered 3rd
        "altered":           "1212222",     # altered dominant, palamidian, super-locrian, locrian with flat 4
        "phrygian dominant": "1312122",     # spanish gypsy, Hijaz - phrygian with raised 3rd
        "harmonic minor":    "2122131",     # natural minor with raised 7th
        "melodic minor":     "2122221",     # ascending only, natural minor with raised 6th and 7th
        "hungarian minor":   "2131131",     # gypsy minor
        "hungarian major":   "3121212",
        "ukranian dorian":   "2131212",     # ukranian minor, romanian minor, altered dorian
        "double harmonic":   "1312131"      # gypsy major
    }
    # TODO add modes of hungarian major scale  https://en.wikipedia.org/wiki/Hungarian_major_scale
    # TODO add modes of double harmonic scale  https://en.wikipedia.org/wiki/Double_harmonic_scale

    SCALE_NAME = {
        "ionian":  "major",
        "aeolian": "minor",
    }

    def _validate_mode(self, mode):
        _mode = mode
        if mode.lower() == "major" or mode == "":
            _mode = "ionian"
        if mode.lower() == "minor" or mode.lower() == "natural minor":
            _mode = "aeolian"

        return super()._validate_mode(_mode)

    def _normalize(self):
        if len(self.notes) == 0:
            return True

        normalized = self.notes.copy()

        next_expected = normalized[0].name()[0]
        for n in normalized:
            if n.name()[0] != next_expected:
                if not self.match_note(next_expected, n.names):
                    return False
                n.use_other_name(next_expected)
            next_expected = self.next_note(next_expected)

        self.notes = normalized
        return True


class OctatonicScale(Scale):
    TYPE = "Octatonic"
    NOTES_CNT = 8
    INTERVALS = {
        "whole tone/half tone": "21212121",
        "half tone/whole tone": "12121212"
    }

    def __str__(self):
        ret = f"{self.root.name()}  {self.TYPE.lower()} {self.mode_name()}: "
        ret += " ".join([x.name() for x in self.notes])
        return ret


class NonatonicScale(Scale):
    TYPE = "Nonatonic"
    NOTES_CNT = 9
    INTERVALS = {
        "blues":  "211122111"
    }

    def _normalize(self):
        if len(self.notes) == 0:
            return True

        if self.mode == "blues":
            heptatonic = HeptatonicScale(self._root_note, "major", self._octave)
            self.notes = heptatonic.notes.copy()
            blue_note_1 = Note(self.notes[0].name()) + 3
            blue_note_1.use_other_name(suggested_root=self.notes[2].name()[0])
            blue_note_2 = Note(self.notes[0].name()) + 10
            blue_note_2.use_other_name(suggested_root=self.notes[6].name()[0])
            self.notes.insert(6, blue_note_2)
            self.notes.insert(2, blue_note_1)
            return True

        return True
