from notes import Note
from intervals import DiatonicInterval


class Chord:
    CHORDS = {
        "":      "",
        "Δ":     "",
        "6":     "⁶",
        "⁶":     "⁶",
        "M6":    "⁶",
        "M⁶":    "⁶",
        "7":     "⁷",
        "⁷":     "⁷",
        "M7":    "M⁷",
        "M⁷":    "M⁷",
        "Δ7":    "M⁷",
        "Δ⁷":    "M⁷",
        "+":     "+",
        "+7":    "+⁷",
        "+⁷":    "+⁷",
        "m":     "m",
        "m6":    "m⁶",
        "m⁶":    "m⁶",
        "m7":    "m⁷",
        "m⁷":    "m⁷",
        "mM7":   "mᴹ⁷",
        "mᴹ⁷":   "mᴹ⁷",
        # "m/M7":  "mᴹ⁷",  # do not use "/" in the chord - conflicts with inversion syntax
        "m(M7)": "mᴹ⁷",
        "o":     "°",
        "°":     "°",
        "o7":    "°⁷",
        "°⁷":    "°⁷",
        "∅":     "∅",
        "%":     "∅",
        "%7":    "∅",
        "∅⁷":    "∅",
        "sus4":  "ˢᵘˢ⁴",
        "ˢᵘˢ⁴":  "ˢᵘˢ⁴",
        "sus2":  "ˢᵘˢ²",
        "ˢᵘˢ²":  "ˢᵘˢ²"
    }

    CHORDS_PROPER_NAMES = {
        "":    "major triad",
        "⁶":   "major 6th chord",
        "⁷":   "dominant 7th chord",
        "M⁷":  "major 7th chord",
        "+":   "augmented triad",
        "+⁷":  "augmented 7th chord",
        "m":   "minor triad",
        "m⁶":  "minor 6th chord",
        "m⁷":  "minor 7th chord",
        "mᴹ⁷": "minor-major 7th chord",
        "°":   "diminished triad",
        "°⁷":  "diminished 7th chord",
        "∅":   "half-diminished 7th chord",
        "ˢᵘˢ⁴": "suspended 4th chord ",
        "ˢᵘˢ²": "suspended 2nd chord"
    }

    CHORD_INTERVALS = {
        "":    ["M3", "P5"],              # major
        "⁶":   ["M3", "P5", "M6"],
        "⁷":   ["M3", "P5", "m7"],
        "M⁷":  ["M3", "P5", "M7"],
        "+":   ["M3", "A5"],
        "+⁷":  ["M3", "A5", "m7"],
        "m":   ["m3", "P5"],              # minor
        "m⁶":  ["m3", "P5", "M6"],
        "m⁷":  ["m3", "P5", "m7"],
        "mᴹ⁷": ["m3", "P5", "M7"],
        "°":   ["m3", "d5"],
        "°⁷":  ["m3", "d5", "d7"],
        "∅":   ["m3", "d5", "m7"],
        "ˢᵘˢ⁴": ["P4", "P5"],
        "ˢᵘˢ²": ["M2", "P5"]
    }

    def __init__(self, chord_name: str = "", octave=4):
        chord = self._validate_name(chord_name)
        self.chord_name = chord["name"]
        self.over = chord["over"]
        self.root = Note(name=chord["root"], octave=octave)
        self.notes = self._chord()

    def name(self):
        ret = self.root.name() + self.chord_name
        if self.over != "":
            ret += "/" + self.over
        return ret

    def _chord(self):
        lst = list()
        lst.append(self.root)
        for i in self.CHORD_INTERVALS[self.chord_name]:
            note = self.root + i
            lst.append(note)

        if self.over != "":
            found = -1
            for idx, note in enumerate(lst):
                if self.over == note.name():
                    found = idx

            if found == -1:
                self.over = ""
                return lst

            for idx in range(found):
                note = lst[idx] + "P8"
                lst.append(note)

            for idx in range(found):
                lst.pop(0)

        return lst

    def _validate_name(self, name):
        # <NoteAcc><Chord>[/<NoteAcc>]

        ret = {"root": "",
               "name": "",
               "over": ""}

        if len(name) == 0:
            return ret

        inv = ""
        if name.find("/") > -1:
            name, inv = name.split("/")

        root_name = name[0].upper()
        if root_name not in Note.NOTES.keys():
            return ret

        acc = name[1:].lower()
        next_idx = 1
        for a in Note.ACCIDENTALS.keys():
            if acc.startswith(a):
                root_name += a
                next_idx += len(a)

        c = name[next_idx:].strip()
        if c not in self.CHORDS.keys():
            return ret

        ret["root"] = root_name
        ret["name"] = self.CHORDS[c]
        if inv != "":
            ret["over"] = Note.validate_name(inv)

        return ret

    def __str__(self):
        ret = self.root.name() + self.chord_name
        if self.over != "":
            ret += "/" + self.over
        ret += ": "
        # ret += " ".join([x.name(octave=(self.over != "")) for x in self.notes])
        ret += " ".join([x.name(octave=True) for x in self.notes])
        return ret

    @classmethod
    def semitones_to_chords(cls):
        ret = {}
        for chord, intervals in Chord.CHORD_INTERVALS.items():
            signature = ""
            for interval in intervals:
                cnt = DiatonicInterval.SEMITONE_CNT.get(interval, None)
                signature += str(cnt)
            ret[signature] = chord

        return ret


if __name__ == "__main__":
    chord = Chord("C")
    print(chord)

    chord = Chord("Cm")
    print(chord)

    chord = Chord("C#")
    print(chord)

    chord = Chord("C#m")
    print(chord)

    chord = Chord("F#")
    print(chord)

    chord = Chord("G")
    print(chord)

    chord = Chord("C/E")
    print(chord)

    chord = Chord("C/G")
    print(chord)

    # for ch in Chord.CHORD_INTERVALS.keys():
    #     chord = Chord("C" + ch)
    #     print(chord)
