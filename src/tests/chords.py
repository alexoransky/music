if __name__ == "__main__":
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from theory.chords import Chord

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
