if __name__ == "__main__":
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from theory.notes import Note

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
