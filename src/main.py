from termcolor import cprint
from theory.chords import Chord
from audio.synth import Synth


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

    # play_scale(synth, HeptatonicScale("C", "major"))
    # play_scale(synth, HeptatonicScale("C", "phrygian"))
    # play_scale(synth, HeptatonicScale("C", "minor"))
    #
    # play_scale(synth, HeptatonicScale("G", "major"))
    # play_scale(synth, HeptatonicScale("G", "phrygian"))
    # play_scale(synth, HeptatonicScale("G", "minor"))
    #
    # play_scale(synth, HeptatonicScale("D", "minor"))
    # play_scale(synth, HeptatonicScale("D", "dorian"))
    # play_scale(synth, HeptatonicScale("D", "phrygian"))

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

    ch_c4 = Chord("C", octave=5)
    ch_c3 = Chord("C", octave=3)
    play_chord(synth, ch_c4)
    play_chord(synth, ch_c3)
    play_notes(synth, ch_c3.notes + ch_c4.notes, chord=True)

    synth.stop(delay_sec=1)
