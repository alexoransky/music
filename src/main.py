from termcolor import cprint
from theory.chords import Chord
from audio.synth import Synth
from theory.scales import PentatonicScale, HexatonicScale, HeptatonicScale, OctatonicScale


def play_notes(synth, notes, chord=False):
    cprint(" ".join([n.name(octave=True) for n in notes]), "blue")
    synth.play(notes, chord=chord)


def play_scale(synth, scale):
    cprint(scale, "blue")
    synth.play(scale.notes)


def play_chord(synth, chord):
    cprint(chord, "blue")
    synth.play(chord.notes, chord=True)


def play_chords(synth, chord_names):
    for ch in chord_names:
        play_chord(synth, Chord(ch))


if __name__ == "__main__":
    synth = Synth()
    synth.start()

    # https: // www.basicmusictheory.com / f - minor - pentatonic - scale

    # play_scale(synth, PentatonicScale("C", "major"))
    play_scale(synth, PentatonicScale("Ab", "natural minor"))
    # play_scale(synth, PentatonicScale("E", "natural minor"))
    # play_scale(synth, PentatonicScale("D", "yo"))           #  D E F𝄪 G𝄪 A𝄪 C𝄪
    # play_scale(synth, PentatonicScale("D", "in"))
    play_scale(synth, PentatonicScale("B", "natural minor"))     #  B D E F♯ A B  # TODO
    play_scale(synth, PentatonicScale("F#", "natural minor"))    #  F♯ A B C♯ E F♯
    # play_scale(synth, PentatonicScale("C#", "natural minor"))
    # play_scale(synth, PentatonicScale("G#", "natural minor"))
    # play_scale(synth, PentatonicScale("D#", "natural minor"))
    # play_scale(synth, PentatonicScale("A#", "natural minor"))
    # play_scale(synth, PentatonicScale("D", "natural minor"))
    play_scale(synth, PentatonicScale("G", "natural minor"))
    # play_scale(synth, PentatonicScale("C", "natural minor"))
    # play_scale(synth, PentatonicScale("F", "natural minor"))
    # play_scale(synth, PentatonicScale("Bb", "natural minor"))
    # play_scale(synth, PentatonicScale("Eb", "natural minor"))
    play_scale(synth, PentatonicScale("Ab", "natural minor"))    # TODO: generates Cb, should be B

    play_scale(synth, HexatonicScale("B"))    #  B C♯ D♯ E♯ F𝄪 G𝄪 A𝄪
    # play_scale(synth, HexatonicScale("C"))  # TODO generates B#- should be C
    # play_scale(synth, HexatonicScale("D"))  # TODO generates C##- should be D

    play_scale(synth, HeptatonicScale("C", "major locrian"))
    play_scale(synth, HeptatonicScale("Cb", "minor"))   #  C♭ D♭ E𝄫 F♭ G♭ A𝄫 B𝄫 C♭
    play_scale(synth, HeptatonicScale("E", "phrygian dominant"))   #  E F G♯ A B C D E
    # play_scale(synth, HeptatonicScale("C", "jazz minor"))
    # play_scale(synth, HeptatonicScale("C", "locrian"))
    # play_scale(synth, HeptatonicScale("C", "altered"))
    # play_scale(synth, HeptatonicScale("E", "minor"))
    # play_scale(synth, HeptatonicScale("E", "harmonic minor"))
    # play_scale(synth, HeptatonicScale("E", "phrygian"))
    # play_scale(synth, HeptatonicScale("E", "phrygian dominant"))
    play_scale(synth, HeptatonicScale("G", "minor"))
    play_scale(synth, HeptatonicScale("Ab", "minor"))
    play_scale(synth, HeptatonicScale("C", "major"))
    # play_scale(synth, HeptatonicScale("C", "phrygian"))
    # play_scale(synth, HeptatonicScale("C", "minor"))
    # play_scale(synth, HeptatonicScale("G", "major"))
    # play_scale(synth, HeptatonicScale("G", "phrygian"))
    # play_scale(synth, HeptatonicScale("D", "minor"))
    # play_scale(synth, HeptatonicScale("D", "dorian"))
    # play_scale(synth, HeptatonicScale("D", "phrygian"))

    # play_scale(synth, OctatonicScale("C#", "w/h"))  # TODO generates Db- should be C#
    # play_scale(synth, OctatonicScale("D", "w/h"))
    # play_scale(synth, OctatonicScale("Eb", "w/h"))


    # play_chords(synth, ["Am7", "Dm7", "C7", "Fm7", "Am7", "D7"])
    # play_chords(synth, ["F", "F", "F", "Cm", "F", "F", "C", "D", "D", "D", "Cm", "D", "D", "C"])

    # for ch in Chord.CHORD_INTERVALS.keys():
    #     chord = Chord("C" + ch)
    #     play_chord(synth, chord)

    # play_chords(synth, ["C/G", "C/E", "C"])

    # play_chords(synth, ["C", "F", "G"])

    # ch_c = Chord("C", octave=4)
    # ch_f = Chord("F", octave=4)
    # ch_g = Chord("G", octave=4)
    # play_chord(synth, ch_c)
    # play_chord(synth, ch_f)
    # play_chord(synth, ch_g)

    # ch_c = Chord("C", octave=4)
    # ch_f = Chord("F/C", octave=3)
    # ch_g = Chord("G", octave=3)
    # play_chord(synth, ch_c)
    # play_chord(synth, ch_f)
    # play_chord(synth, ch_g)

    # ch_c4 = Chord("C", octave=5)
    # ch_c3 = Chord("C", octave=3)
    # play_chord(synth, ch_c4)
    # play_chord(synth, ch_c3)
    # play_notes(synth, ch_c3.notes + ch_c4.notes, chord=True)

    synth.stop(delay_sec=1)
