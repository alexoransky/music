import unittest
from theory.scales import PentatonicScale, HexatonicScale, HeptatonicScale

# see the following website for test reference:
# https://www.basicmusictheory.com/f-sharp-harmonic-minor-scale


class TestHeptatonicScale(unittest.TestCase):
    def test_C(self):
        scale = HeptatonicScale("C")
        self.assertEqual(scale.name(), "C major")
        self.assertEqual(scale.mode_name(), "ionian")
        self.assertEqual(scale.note_names(), "C D E F G A B")

    def test_B_major(self):
        scale = HeptatonicScale("B", "major")
        self.assertEqual(scale.name(), "B major")
        self.assertEqual(scale.mode_name(), "ionian")
        self.assertEqual(scale.note_names(), "B C♯ D♯ E F♯ G♯ A♯")

    def test_C_minor(self):
        scale = HeptatonicScale("C", "minor")
        self.assertEqual(scale.name(), "C minor")
        self.assertEqual(scale.mode_name(), "aeolian")
        self.assertEqual(scale.note_names(), "C D E♭ F G A♭ B♭")

    def test_C_natural_minor(self):
        scale = HeptatonicScale("C", "natural minor")
        self.assertEqual(scale.name(), "C minor")
        self.assertEqual(scale.mode_name(), "aeolian")
        self.assertEqual(scale.note_names(), "C D E♭ F G A♭ B♭")

    def test_E_natural_minor(self):
        scale = HeptatonicScale("E", "natural minor")
        self.assertEqual(scale.name(), "E minor")
        self.assertEqual(scale.mode_name(), "aeolian")
        self.assertEqual(scale.note_names(), "E F♯ G A B C D")

    def test_E_harmonic_minor(self):
        scale = HeptatonicScale("E", "harmonic minor")
        self.assertEqual(scale.name(), "E harmonic minor")
        self.assertEqual(scale.mode_name(), "harmonic minor")
        self.assertEqual(scale.note_names(), "E F♯ G A B C D♯")

    def test_E_melodic_minor(self):
        scale = HeptatonicScale("E", "melodic minor")
        self.assertEqual(scale.name(), "E melodic minor")
        self.assertEqual(scale.mode_name(), "melodic minor")
        self.assertEqual(scale.note_names(), "E F♯ G A B C♯ D♯")

    def test_Cb_minor(self):
        scale = HeptatonicScale("Cb", "minor")
        self.assertEqual(scale.name(), "C♭ minor")
        self.assertEqual(scale.mode_name(), "aeolian")
        self.assertEqual(scale.note_names(), "C♭ D♭ E𝄫 F♭ G♭ A𝄫 B𝄫")

    def test_Ab_aeolian(self):
        scale = HeptatonicScale("Ab", "aeolian")
        self.assertEqual(scale.name(), "A♭ minor")
        self.assertEqual(scale.mode_name(), "aeolian")
        self.assertEqual(scale.note_names(), "A♭ B♭ C♭ D♭ E♭ F♭ G♭")

    def test_Ab_aolian(self):
        # misspelled mode "aeolian"
        scale = HeptatonicScale("Ab", "aolian")
        self.assertEqual(scale.name(), "A♭ unknown")
        self.assertEqual(scale.mode_name(), "unknown")
        self.assertEqual(scale.note_names(), "")

    def test_Fs_harmonic_minor(self):
        scale = HeptatonicScale("F#", "harmonic minor")
        self.assertEqual(scale.name(), "F♯ harmonic minor")
        self.assertEqual(scale.mode_name(), "harmonic minor")
        self.assertEqual(scale.note_names(), "F♯ G♯ A B C♯ D E♯")

    def test_Eb_locrian(self):
        scale = HeptatonicScale("Eb", "locrian")
        self.assertEqual(scale.name(), "E♭ locrian")
        self.assertEqual(scale.mode_name(), "locrian")
        self.assertEqual(scale.note_names(), "E♭ F♭ G♭ A♭ B𝄫 C♭ D♭")

    def test_C_locrian(self):
        scale = HeptatonicScale("C", "locrian")
        self.assertEqual(scale.name(), "C locrian")
        self.assertEqual(scale.mode_name(), "locrian")
        self.assertEqual(scale.note_names(), "C D♭ E♭ F G♭ A♭ B♭")

    def test_C_major_locrian(self):
        scale = HeptatonicScale("C", "major locrian")
        self.assertEqual(scale.name(), "C major locrian")
        self.assertEqual(scale.mode_name(), "major locrian")
        self.assertEqual(scale.note_names(), "C D E F G♭ A♭ B♭")

    def test_C_altered(self):
        scale = HeptatonicScale("C", "altered")
        self.assertEqual(scale.name(), "C altered")
        self.assertEqual(scale.mode_name(), "altered")
        self.assertEqual(scale.note_names(), "C D♭ E♭ F♭ G♭ A♭ B♭")

    def test_C_phrygian(self):
        scale = HeptatonicScale("C", "phrygian")
        self.assertEqual(scale.name(), "C phrygian")
        self.assertEqual(scale.mode_name(), "phrygian")
        self.assertEqual(scale.note_names(), "C D♭ E♭ F G A♭ B♭")

    def test_E_phrygian(self):
        scale = HeptatonicScale("E", "phrygian")
        self.assertEqual(scale.name(), "E phrygian")
        self.assertEqual(scale.mode_name(), "phrygian")
        self.assertEqual(scale.note_names(), "E F G A B C D")

    def test_E_phrygian_dominant(self):
        scale = HeptatonicScale("E", "phrygian dominant")
        self.assertEqual(scale.name(), "E phrygian dominant")
        self.assertEqual(scale.mode_name(), "phrygian dominant")
        self.assertEqual(scale.note_names(), "E F G♯ A B C D")

    def test_Gs_ionian(self):
        scale = HeptatonicScale("G#", "ionian")
        self.assertEqual(scale.name(), "G♯ major")
        self.assertEqual(scale.mode_name(), "ionian")
        self.assertEqual(scale.note_names(), "G♯ A♯ B♯ C♯ D♯ E♯ F𝄪")

    def test_Gs_dorian(self):
        scale = HeptatonicScale("G#", "dorian")
        self.assertEqual(scale.name(), "G♯ dorian")
        self.assertEqual(scale.mode_name(), "dorian")
        self.assertEqual(scale.note_names(), "G♯ A♯ B C♯ D♯ E♯ F♯")

    def test_Db_dorian(self):
        scale = HeptatonicScale("D♭", "dorian")
        self.assertEqual(scale.name(), "D♭ dorian")
        self.assertEqual(scale.mode_name(), "dorian")
        self.assertEqual(scale.note_names(), "D♭ E♭ F♭ G♭ A♭ B♭ C♭")

    def test_Bb_mixolydian(self):
        scale = HeptatonicScale("Bb", "mixolydian")
        self.assertEqual(scale.name(), "B♭ mixolydian")
        self.assertEqual(scale.mode_name(), "mixolydian")
        self.assertEqual(scale.note_names(), "B♭ C D E♭ F G A♭")

    def test_Bb_lydian(self):
        scale = HeptatonicScale("Bb", "lydian")
        self.assertEqual(scale.name(), "B♭ lydian")
        self.assertEqual(scale.mode_name(), "lydian")
        self.assertEqual(scale.note_names(), "B♭ C D E F G A")

    def test_Cs_lydian(self):
        scale = HeptatonicScale("C♯", "lydian")
        self.assertEqual(scale.name(), "C♯ lydian")
        self.assertEqual(scale.mode_name(), "lydian")
        self.assertEqual(scale.note_names(), "C♯ D♯ E♯ F𝄪 G♯ A♯ B♯")

    def test_C_jazz_minor(self):
        scale = HeptatonicScale("C", "jazz minor")
        self.assertEqual(scale.name(), "C jazz minor")
        self.assertEqual(scale.mode_name(), "jazz minor")
        self.assertEqual(scale.note_names(), "C D E♭ F G A B")

    def test_C_hungarian_minor(self):
        scale = HeptatonicScale("C", "hungarian minor")
        self.assertEqual(scale.name(), "C hungarian minor")
        self.assertEqual(scale.mode_name(), "hungarian minor")
        self.assertEqual(scale.note_names(), "C D E♭ F♯ G A♭ B")

    def test_C_hungarian_major(self):
        scale = HeptatonicScale("C", "hungarian major")
        self.assertEqual(scale.name(), "C hungarian major")
        self.assertEqual(scale.mode_name(), "hungarian major")
        self.assertEqual(scale.note_names(), "C D♯ E F♯ G A B♭")

    def test_B_ukranian_dorian(self):
        scale = HeptatonicScale("B", "ukranian dorian")
        self.assertEqual(scale.name(), "B ukranian dorian")
        self.assertEqual(scale.mode_name(), "ukranian dorian")
        self.assertEqual(scale.note_names(), "B C♯ D E♯ F♯ G♯ A")

    def test_C_double_harmonic(self):
        scale = HeptatonicScale("C", "double harmonic")
        self.assertEqual(scale.name(), "C double harmonic")
        self.assertEqual(scale.mode_name(), "double harmonic")
        self.assertEqual(scale.note_names(), "C D♭ E F G A♭ B")


class TestPentatonicScale(unittest.TestCase):
    def test_C_minor(self):
        scale = PentatonicScale("C", "minor")
        self.assertEqual(scale.name(), "C minor pentatonic")
        self.assertEqual(scale.mode_name(), "aeolian")
        self.assertEqual(scale.note_names(), "C E♭ F G B♭")

    def test_A_minor(self):
        scale = PentatonicScale("A", "minor")
        self.assertEqual(scale.name(), "A minor pentatonic")
        self.assertEqual(scale.mode_name(), "aeolian")
        self.assertEqual(scale.note_names(), "A C D E G")

    def test_B_natural_minor(self):
        scale = PentatonicScale("B", "minor")
        self.assertEqual(scale.name(), "B minor pentatonic")
        self.assertEqual(scale.mode_name(), "aeolian")
        self.assertEqual(scale.note_names(), "B D E F♯ A")

    def test_E_minor(self):
        scale = PentatonicScale("E", "minor")
        self.assertEqual(scale.name(), "E minor pentatonic")
        self.assertEqual(scale.mode_name(), "aeolian")
        self.assertEqual(scale.note_names(), "E G A B D")

    def test_Ab_natural_minor(self):
        scale = PentatonicScale("Ab", "natural minor")
        self.assertEqual(scale.name(), "A♭ minor pentatonic")
        self.assertEqual(scale.mode_name(), "aeolian")
        self.assertEqual(scale.note_names(), "A♭ C♭ D♭ E♭ G♭")

    def test_C(self):
        scale = PentatonicScale("C")
        self.assertEqual(scale.name(), "C major pentatonic")
        self.assertEqual(scale.mode_name(), "ionian")
        self.assertEqual(scale.note_names(), "C D E G A")

    def test_C_major(self):
        scale = PentatonicScale("C", "major")
        self.assertEqual(scale.name(), "C major pentatonic")
        self.assertEqual(scale.mode_name(), "ionian")
        self.assertEqual(scale.note_names(), "C D E G A")

    def test_Cb_ionian(self):
        scale = PentatonicScale("Cb", "ionian")
        self.assertEqual(scale.name(), "C♭ major pentatonic")
        self.assertEqual(scale.mode_name(), "ionian")
        self.assertEqual(scale.note_names(), "C♭ D♭ E♭ G♭ A♭")

    def test_D_dorian(self):
        scale = PentatonicScale("D", "dorian")
        self.assertEqual(scale.name(), "D egyptian (suspended)")
        self.assertEqual(scale.mode_name(), "dorian")
        self.assertEqual(scale.note_names(), "D E G A C")

    def test_E_prygian(self):
        scale = PentatonicScale("E", "phrygian")
        self.assertEqual(scale.name(), "E blues minor")
        self.assertEqual(scale.mode_name(), "phrygian")
        self.assertEqual(scale.note_names(), "E G A C D")

    def test_As_mixolydian(self):
        scale = PentatonicScale("A#", "mixolydian")
        self.assertEqual(scale.name(), "A♯ blues major")
        self.assertEqual(scale.mode_name(), "mixolydian")
        self.assertEqual(scale.note_names(), "A♯ B♯ D♯ E♯ F𝄪")

    def test_Fs_aeolian(self):
        scale = PentatonicScale("F#", "aeolian")
        self.assertEqual(scale.name(), "F♯ minor pentatonic")
        self.assertEqual(scale.mode_name(), "aeolian")
        self.assertEqual(scale.note_names(), "F♯ A B C♯ E")


class TestHexatonicScale(unittest.TestCase):
    def test_C_whole_tone(self):
        scale = HexatonicScale("C", "whole tone")
        self.assertEqual(scale.name(), "C whole tone")
        self.assertEqual(scale.mode_name(), "whole tone")
        self.assertEqual(scale.note_names(), "C D E F♯ G♯ A♯")

    def test_Db_whole_tone(self):
        scale = HexatonicScale("Db", "whole tone")
        self.assertEqual(scale.name(), "D♭ whole tone")
        self.assertEqual(scale.mode_name(), "whole tone")
        self.assertEqual(scale.note_names(), "D♭ E♭ F G A B")

    def test_C_major(self):
        scale = HexatonicScale("C", "major")
        self.assertEqual(scale.name(), "C major hexatonic")
        self.assertEqual(scale.mode_name(), "major")
        self.assertEqual(scale.note_names(), "C D E F G A")

    def test_C_minor(self):
        scale = HexatonicScale("C", "minor")
        self.assertEqual(scale.name(), "C minor hexatonic")
        self.assertEqual(scale.mode_name(), "minor")
        self.assertEqual(scale.note_names(), "C D E♭ F G B♭")

    def test_C_augmented(self):
        scale = HexatonicScale("C", "augmented")
        self.assertEqual(scale.name(), "C augmented")
        self.assertEqual(scale.mode_name(), "augmented")
        self.assertEqual(scale.note_names(), "C D♯ E F𝄪 G♯ A𝄪")    #  C E♭ E G G♯ B

    def test_C_blues(self):
        scale = HexatonicScale("C", "blues")
        self.assertEqual(scale.name(), "C blues")
        self.assertEqual(scale.mode_name(), "blues")
        self.assertEqual(scale.note_names(), "C E♭ F G♭ G B♭")

    def test_Ds_blues(self):
        scale = HexatonicScale("D#", "blues")
        self.assertEqual(scale.name(), "D♯ blues")
        self.assertEqual(scale.mode_name(), "blues")
        self.assertEqual(scale.note_names(), "D♯ F♯ G♯ A A♯ C♯")


if __name__ == "__main__":
    unittest.main()