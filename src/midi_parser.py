import re
from dataclasses import dataclass

from chords import Chord
from notes import Note


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
    def __init__(self):
        self.chords = Chord.semitones_to_chords()
        self.notes = set()

    def print_notes(self):
        note_list = sorted(list(self.notes))
        if len(note_list) >= 3:
            st = self.semitones(note_list)
            chord = self.chords.get(st, None)
            n0 = Note(midi_number=note_list[0])
            if chord is not None:
                print(Chord(n0.name() + chord, n0.octave))
        else:
            for n in note_list:
                print(Note(midi_number=n).name(octave=True))

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
            self.notes.add(int(n.group(NOTE)))
            self.print_notes()
            return

        n = re.search(NOTE_OFF_RE, msg)
        if n is not None:
            # note = MIDINote(int(n.group(CHANNEL)), int(n.group(NOTE)), int(n.group(VELOCITY)))
            self.notes.remove(int(n.group(NOTE)))
            return

    def semitones(self, notes):
        if len(notes) < 3:
            return None

        signature = ""
        n0 = notes[0]
        for i in range(1, len(notes)):
            signature += str(notes[i] - n0)

        return signature
