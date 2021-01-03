class Temperament:
    NOTE_TO_NUMBER = {}
    NUMBER_TO_NOTE = []

    @classmethod
    def note_to_number(cls, note):
        """
        :returns note number within the octave, 0-based (C)
        """
        return cls.NOTE_TO_NUMBER[note]

    @classmethod
    def number_to_note(cls, number):
        """
        :returns tuple note names within the octave, 0-based (C)
        """
        return cls.NUMBER_TO_NOTE[number]


class TET12(Temperament):
    NOTE_TO_NUMBER = {
        "B♯": 0,
        "C":  0,
        "C♯": 1,
        "D♭": 1,
        "D":  2,
        "D♯": 3,
        "E♭": 3,
        "E":  4,
        "F♭": 4,
        "E♯": 5,
        "F":  5,
        "F♯": 6,
        "G♭": 6,
        "G":  7,
        "G♯": 8,
        "A♭": 8,
        "A":  9,
        "A♯": 10,
        "B♭": 10,
        "B":  11,
        "C♭": 11
    }

    NUMBER_TO_NOTE = [
        ("C",  "B♯", "D𝄫"),
        ("C♯", "B𝄪", "D♭"),
        ("D",  "C𝄪", "E𝄫"),
        ("D♯", "E♭", "F𝄫"),
        ("E",  "D𝄪", "F♭"),
        ("F",  "E♯", "G𝄫"),
        ("F♯", "E𝄪", "G♭"),
        ("G",  "F𝄪", "A𝄫"),
        ("G♯", "A♭"),
        ("A",  "G𝄪", "B𝄫"),
        ("A♯", "B♭", "C𝄫"),
        ("B",  "A𝄪", "C♭")
    ]
