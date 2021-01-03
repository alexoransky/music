import math

from .intervals import DiatonicInterval
from .temperaments import TET12
from .validate import validate_int

NOTE_A_FREQ_HZ = 440
SUBSCRIPT_0 = 8320


# MIDI note numbers are 0 to 127
# Piano keys range is 21 (A0) to 108 (C8) of MIDI range

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

        self.note_a_freq_hz = NOTE_A_FREQ_HZ

        if midi_number is not None:
            self._create_from_midi(midi_number, suggested_root)
            return

        self.names = [self.validate_name(name)]
        self.octave = validate_int(octave, -1, 9)
        self.number = 12*(self.octave+1) + TET12.note_to_number(self.names[0])

    def _create_from_midi(self, midi_number: int, suggested_root: str = None):
        if midi_number < 0:
            return

        self.names = TET12.number_to_note(midi_number % 12)
        self.octave = midi_number//12 - 1
        self.number = midi_number
        if suggested_root is not None:
            if self.name()[0] != suggested_root:
                self.use_other_name(suggested_root)

    def set_note_a_freq(self, freq_hz):
        self.note_a_freq_hz = freq_hz

    def freq_hz(self):
        return self.note_a_freq_hz * math.pow(2, (self.number-69)/12)

    def name(self, octave=False):
        ret = self.names[self._name_idx]
        if octave:
            if self.octave > -1:
                octave_chr = chr(SUBSCRIPT_0 + self.octave)
            else:
                # -1
                octave_chr = chr(SUBSCRIPT_0 + 11) + chr(SUBSCRIPT_0 + abs(self.octave))
            ret += octave_chr
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
    def midi_number_to_note_name(cls, midi_number):
        # returns note name with no flats (C4, C♯4 and so on)
        name = TET12.number_to_note(midi_number % 12)[0]
        octave = midi_number//12 - 1
        if octave > -1:
            octave_chr = chr(SUBSCRIPT_0 + octave)
        else:
            # -1
            octave_chr = chr(SUBSCRIPT_0 + 11) + chr(SUBSCRIPT_0 + abs(octave))
        return name + octave_chr

    @classmethod
    def note_name_to_midi_number(cls, note_name):
        octave = note_name[-1:]
        name = cls.validate_name(note_name[:-1])
        return (int(octave) + 1) * 12 + TET12.note_to_number(name)

    @classmethod
    def note_name_to_freq_hz(cls, note_name, note_a_freq_hz=440.0):
        midi_number = Note.note_name_to_midi_number(note_name)
        return Note.midi_number_to_freq_hz(midi_number, note_a_freq_hz=note_a_freq_hz)

    @classmethod
    def midi_number_to_freq_hz(cls, midi_number, note_a_freq_hz=440.0):
        f = note_a_freq_hz * math.pow(2, (midi_number - 69) / 12)
        f_prev = note_a_freq_hz * math.pow(2, (midi_number - 70) / 12)
        f_next = note_a_freq_hz * math.pow(2, (midi_number - 68) / 12)
        return f, (f+f_prev)/2, (f+f_next)/2

    @classmethod
    def freq_to_midi_number(cls, freq_hz, note_a_freq_hz=440.0):
        midi_number = 69 + 12 * math.log2(freq_hz/note_a_freq_hz)
        if (midi_number - int(midi_number)) > 0.5:
            midi_number += 1
        return int(midi_number)

    @classmethod
    def freq_to_note_name(cls, freq_hz, note_a_freq_hz=440.0):
        midi_number = Note.freq_to_midi_number(freq_hz, note_a_freq_hz=note_a_freq_hz)
        return Note.midi_number_to_note_name(midi_number)

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
