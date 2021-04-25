import unittest
from theory.scales import HeptatonicScale

# see the following website for test reference:
# https://www.basicmusictheory.com/f-sharp-harmonic-minor-scale


class TestHeptatonicScale(unittest.TestCase):
    def test_C(self):
        scale = HeptatonicScale("C")
        self.assertEqual(scale.name(), "C ionian")
        self.assertEqual(scale.note_names(), "C D E F G A B C")

    def test_B_major(self):
        scale = HeptatonicScale("B", "major")
        self.assertEqual(scale.name(), "B ionian")
        self.assertEqual(scale.note_names(), "B C♯ D♯ E F♯ G♯ A♯ B")

    def test_E_natural_minor(self):
        scale = HeptatonicScale("E", "natural minor")
        self.assertEqual(scale.name(), "E aeolian")
        self.assertEqual(scale.note_names(), "E F♯ G A B C D E")

    def test_E_harmonic_minor(self):
        scale = HeptatonicScale("E", "harmonic minor")
        self.assertEqual(scale.name(), "E harmonic minor")
        self.assertEqual(scale.note_names(), "E F♯ G A B C D♯ E")

    def test_E_melodic_minor(self):
        scale = HeptatonicScale("E", "melodic minor")
        self.assertEqual(scale.name(), "E melodic minor")
        self.assertEqual(scale.note_names(), "E F♯ G A B C♯ D♯ E")

    def test_Cb_minor(self):
        scale = HeptatonicScale("Cb", "minor")
        self.assertEqual(scale.name(), "C♭ aeolian")
        self.assertEqual(scale.note_names(), "C♭ D♭ E𝄫 F♭ G♭ A𝄫 B𝄫 C♭")

    def test_Ab_aeolian(self):
        scale = HeptatonicScale("Ab", "aeolian")
        self.assertEqual(scale.name(), "A♭ aeolian")
        self.assertEqual(scale.note_names(), "A♭ B♭ C♭ D♭ E♭ F♭ G♭ A♭")

    def test_Ab_aolian(self):
        # misspelled mode "aeolian"
        scale = HeptatonicScale("Ab", "aolian")
        self.assertEqual(scale.name(), "A♭ unknown")
        self.assertEqual(scale.note_names(), "")

    def test_Fs_harmonic_minor(self):
        scale = HeptatonicScale("F#", "harmonic minor")
        self.assertEqual(scale.name(), "F♯ harmonic minor")
        self.assertEqual(scale.note_names(), "F♯ G♯ A B C♯ D E♯ F♯")

    def test_Eb_locrian(self):
        scale = HeptatonicScale("Eb", "locrian")
        self.assertEqual(scale.name(), "E♭ locrian")
        self.assertEqual(scale.note_names(), "E♭ F♭ G♭ A♭ B𝄫 C♭ D♭ E♭")

    def test_C_locrian(self):
        scale = HeptatonicScale("C", "locrian")
        self.assertEqual(scale.name(), "C locrian")
        self.assertEqual(scale.note_names(), "C D♭ E♭ F G♭ A♭ B♭ C")

    def test_C_major_locrian(self):
        scale = HeptatonicScale("C", "major locrian")
        self.assertEqual(scale.name(), "C major locrian")
        self.assertEqual(scale.note_names(), "C D E F G♭ A♭ B♭ C")

    def test_C_altered(self):
        scale = HeptatonicScale("C", "altered")
        self.assertEqual(scale.name(), "C altered")
        self.assertEqual(scale.note_names(), "C D♭ E♭ F♭ G♭ A♭ B♭ C")

    def test_C_phrygian(self):
        scale = HeptatonicScale("C", "phrygian")
        self.assertEqual(scale.name(), "C phrygian")
        self.assertEqual(scale.note_names(), "C D♭ E♭ F G A♭ B♭ C")

    def test_E_phrygian(self):
        scale = HeptatonicScale("E", "phrygian")
        self.assertEqual(scale.name(), "E phrygian")
        self.assertEqual(scale.note_names(), "E F G A B C D E")

    def test_E_phrygian_dominant(self):
        scale = HeptatonicScale("E", "phrygian dominant")
        self.assertEqual(scale.name(), "E phrygian dominant")
        self.assertEqual(scale.note_names(), "E F G♯ A B C D E")

    def test_C_jazz_minor(self):
        scale = HeptatonicScale("C", "jazz minor")
        self.assertEqual(scale.name(), "C jazz minor")
        self.assertEqual(scale.note_names(), "C D E♭ F G A B C")

    def test_C_hungarian_minor(self):
        scale = HeptatonicScale("C", "hungarian minor")
        self.assertEqual(scale.name(), "C hungarian minor")
        self.assertEqual(scale.note_names(), "C D E♭ F♯ G A♭ B C")

    def test_C_hungarian_major(self):
        scale = HeptatonicScale("C", "hungarian major")
        self.assertEqual(scale.name(), "C hungarian major")
        self.assertEqual(scale.note_names(), "C D♯ E F♯ G A B♭ C")

    def test_B_ukranian_dorian(self):
        scale = HeptatonicScale("B", "ukranian dorian")
        self.assertEqual(scale.name(), "B ukranian dorian")
        self.assertEqual(scale.note_names(), "B C♯ D E♯ F♯ G♯ A B")

    def test_C_double_harmonic(self):
        scale = HeptatonicScale("C", "double harmonic")
        self.assertEqual(scale.name(), "C double harmonic")
        self.assertEqual(scale.note_names(), "C D♭ E F G A♭ B C")


if __name__ == "__main__":
    unittest.main()