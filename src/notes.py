import math
from intervals import DiatonicInterval
from temperaments import TET12
from validate_utils import validate_int

tet12 = TET12()
SUBSCRIPT_0 = 8320


# MIDI note numbers are 0 to 127
# Piano keys range is 21 to 108 of MIDI range

class Note:
    NOTES = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
    ACCIDENTALS = {
        "♯": "♯",
        "#": "♯",
        "sharp": "♯",
        "s": "♯",
        "♭": "♭",
        "flat": "♭",
        "b": "♭"}

    A_FREQ_HZ = 440

    def __init__(self, name: str = "", octave: int = 4, midi_number: int = None, suggested_root: str = None):
        """
        create a not from name/octave or the MIDI number
        :param name: note name e.g. A sharp, C, B♭
        :param octave: int from -1 to 9
        :param midi_number: NoteOn MIDI number, int 0 (C of -1 octave), 1, etc
        """

        # 12-TET has the same pitch for C♯ and D♭ etc.
        # they are saved in names list
        self.names = None
        self._name_idx = 0

        # note number in the 12-TET, based on MIDI
        # based on note C of -1 octave
        # range is 0.. Note that 0..127 is a valid NoteOn MIDI number, 128.. - extended part
        self.number = None
        self.octave = None

        if midi_number is not None:
            self._create_from_midi(midi_number, suggested_root)
            return

        self.names = [self.validate_name(name)]
        self.octave = validate_int(octave, -1, 9)
        self.number = 12*(self.octave+1) + tet12.note_to_number(self.names[0])

    def _create_from_midi(self, midi_number: int, suggested_root: str = None):
        if midi_number < 0:
            return

        self.names = tet12.number_to_note(midi_number % 12)
        self.octave = midi_number//12 - 1
        self.number = midi_number
        if suggested_root is not None:
            if self.name()[0] != suggested_root:
                self.use_other_name(suggested_root)

    def freq_hz(self):
        return self.A_FREQ_HZ * math.pow(2, (self.number-69)/12)

    def name(self, octave=False):
        ret = self.names[self._name_idx]
        if octave:
            ret += chr(SUBSCRIPT_0 + self.octave)
        return ret

    def use_other_name(self, suggested_root=None):
        if suggested_root is not None:
            for idx, name in enumerate(self.names):
                if name[0] == suggested_root:
                    self._name_idx = idx
                    return

        self._name_idx += 1
        if self._name_idx > len(self.names):
            self._name_idx = 0

    @classmethod
    def validate_name(cls, name):
        if len(name) == 0:
            return ""

        n = name[0].upper()
        if n in cls.NOTES.keys():
            ret_name = name[0].upper()
        else:
            return ""
        if len(name) == 1:
            return ret_name

        a = name[1:].lower().strip()
        if a in cls.ACCIDENTALS.keys():
            ret_name += cls.ACCIDENTALS[a]

        return ret_name

    def __add__(self, interval):
        cnt = None
        root = None

        if isinstance(interval, int):
            cnt = interval

        if isinstance(interval, str):
            cnt = DiatonicInterval.SEMITONE_CNT[interval]
            degrees = DiatonicInterval(interval).degrees() - 1
            new_idx = (self.NOTES[self.name()[0]] + degrees) % len(self.NOTES)
            root = list(self.NOTES.keys())[new_idx]

        if cnt is None:
            return None

        return Note(midi_number=(self.number + cnt), suggested_root=root)

    def __radd__(self, interval):
        return self.__add__(interval)

    def __sub__(self, interval):
        cnt = None
        root = None

        if isinstance(interval, int):
            cnt = interval

        if isinstance(interval, str):
            cnt = DiatonicInterval.SEMITONE_CNT[interval]
            degrees = DiatonicInterval(interval).degrees() - 1
            new_idx = (self.NOTES[self.name()[0]] - degrees) % len(self.NOTES)
            root = list(self.NOTES.keys())[new_idx]

        if cnt is None:
            return None

        return Note(midi_number=(self.number - cnt), suggested_root=root)

    def __str__(self):
        if len(self.names) == 0:
            return None

        ret = self.names[0]
        if len(self.names) > 1:
            ret += " ("
            ret += ", ".join(self.names[1:])
            ret += ")"
        return ret


if __name__ == "__main__":
    note = Note("D#", octave=5)
    print(note)
    print(note.name())
    print(note.number)
    print(note.freq_hz())

    note += 2
    print(note)
    print(note.name())
    print(note.number)
    print(note.freq_hz())

    note = Note(midi_number=21)
    print(note.name())
    print(note.number)
    print(note.freq_hz())

    note += 5
    print(note.name())
    print(note.number)
    print(note.freq_hz())

    note += "M3"
    print(note.name())
    print(note.number)
    print(note.freq_hz())

    note = note + 1
    print(note.name())
    print(note.number)
    print(note.freq_hz())

    note = note - 1
    print(note.name())
    print(note.number)
    print(note.freq_hz())

    note = 2 + note
    print(note.name())
    print(note.number)
    print(note.freq_hz())

    note += "P8"
    print(note.name(octave=True))
    print(note.number)
    print(note.freq_hz())
