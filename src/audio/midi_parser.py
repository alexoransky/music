import re
from dataclasses import dataclass

from theory.chords import Chord
from theory.notes import Note


CHANNEL = "channel"
NOTE = "note"
VELOCITY = "velocity"
NOTE_ON = "note_on"
NOTE_OFF = "note_off"
CHANNEL_RE = f"(?P<{CHANNEL}>" + "[0-9]{1,2})"
NOTE_RE = f"(?P<{NOTE}>" + "[0-9]{1,3})"
VELOCITY_RE = f"(?P<{VELOCITY}>" + "[0-9]{1,3})"

# note_on channel=0 note=55 velocity=64 time=0
NOTE_ON_RE = f"^({NOTE_ON}) ({CHANNEL}=){CHANNEL_RE} ({NOTE}=){NOTE_RE} ({VELOCITY}=){VELOCITY_RE}"

# note_off channel=0 note=55 velocity=64 time=0
NOTE_OFF_RE = f"^({NOTE_OFF}) ({CHANNEL}=){CHANNEL_RE} ({NOTE}=){NOTE_RE} ({VELOCITY}=){VELOCITY_RE}"


@dataclass
class MIDINote:
    channel: int
    note: int
    velocity: int


class MIDIParser:
    def __init__(self, enable_print=True):
        self.print = enable_print
        self.chords = Chord.semitones_to_chords()
        self.notes = set()
        self.note_fn = None

    def get_notes(self, midi_notes_set):
        midi_notes = sorted(list(midi_notes_set))
        notes = []
        chord = None
        for n in midi_notes:
            note = Note(midi_number=n)
            notes.append(note)
        if len(midi_notes) >= 3:
            st = self.semitones(midi_notes)
            chord = self.chords.get(st, None)
        return notes, chord

    def print_notes(self):
        notes, chord = self.get_notes(self.notes)
        if chord is not None:
            print(Chord(notes[0].name() + chord, notes[0].octave))
        for note in notes:
            print(note.name(octave=True), note.number)

    def set_note_on_off_fn(self, note_fn):
        self.note_fn = note_fn

    def parse(self, message):
        """
        :param message:
        :return:
        """
        if message is None:
            return

        msg = str(message)

        n = re.search(NOTE_ON_RE, msg)
        if n is not None:
            # note = MIDINote(int(n.group(CHANNEL)), int(n.group(NOTE)), int(n.group(VELOCITY)))
            note_num = int(n.group(NOTE))
            self.notes.add(note_num)
            if self.print:
                self.print_notes()

            if self.note_fn is not None:
                self.note_fn(note_num, True)
            return

        if len(self.notes) == 0:
            return

        n = re.search(NOTE_OFF_RE, msg)
        if n is not None:
            # note = MIDINote(int(n.group(CHANNEL)), int(n.group(NOTE)), int(n.group(VELOCITY)))
            note_num = int(n.group(NOTE))
            self.notes.remove(note_num)
            if self.note_fn is not None:
                self.note_fn(note_num, False)
            return

    @classmethod
    def semitones(cls, notes):
        if len(notes) < 3:
            return None

        signature = ""
        n0 = notes[0]
        for i in range(1, len(notes)):
            signature += str(notes[i] - n0)

        return signature
