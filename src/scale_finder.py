import sys
from termcolor import cprint, colored
from theory.scales import HeptatonicScale, PentatonicScale
from theory.temperaments import TET12
from theory.notes import Note
from pprint import pprint


NOTES_TO_EXCLUDE = ["B♯", "E♯", "C♭", "F♭"]


def find_scales(notes, pentatonic=True, modes=False):
    def note_in_scale(n, s):
        # print(n, s)
        ret = False
        for sn in s.notes:
            # print(n, sn.names)
            if n in sn.names:
                ret = True
                break
        # print(ret)
        return ret

    if pentatonic:
        scale_type = PentatonicScale
    else:
        scale_type = HeptatonicScale

    scales = []
    for note in TET12.NOTE_TO_NUMBER.keys():
        if note in NOTES_TO_EXCLUDE:
            continue
        if modes:
            for mode in scale_type.DIATONIC_INTERVALS.keys():
                scales.append(scale_type(note, mode=mode))
        else:
            scales.append(scale_type(note, mode="major"))
            scales.append(scale_type(note, mode="natural minor"))

    ret = []
    for scale in scales:
        add = True
        for note in notes:
            if not note_in_scale(note, scale):
                add = False
                break
        if add:
            ret.append(scale)

    return ret


if __name__ == "__main__":
    if len(sys.argv) < 1:
        exit()

    scale_type = "heptatonic"
    all_modes = False
    note_input = False
    notes = []
    for n in range(1, len(sys.argv)):
        if sys.argv[n].lower() == "-p":
            scale_type = "pentatonic"
            continue
        if sys.argv[n].lower() == "-m":
            all_modes = True
            continue
        if sys.argv[n].lower() == "-n":
            note_input = True
            continue
        if sys.argv[n].lower() == "-c":
            note_input = False
            continue
        note = Note.validate_name(sys.argv[n])
        if note != "":
            notes.append(note)

    scales = find_scales(notes, pentatonic=(scale_type == "pentatonic"), modes=all_modes)
    if len(scales) > 0:
        print(f"Notes {notes} belong to the following {scale_type} scales:")
        for scale in scales:
            sn = colored(scale.name(), "blue")
            ns = colored(scale.note_names(), "blue")
            print(f"{sn:<26} {ns}")
    else:
        cprint(f"No scales found for notes {notes}", "red")