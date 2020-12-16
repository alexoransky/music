import pygame.midi
import time
from termcolor import cprint
from theory.scales import HeptatonicScale

DEVICE = 0
INSTRUMENT = 1  # http://www.ccarh.org/courses/253/handout/gminstruments/


def play(player, notes, volume=10, wait=0.3):
    for note in notes:
        player.note_on(note.number, volume)
        time.sleep(wait)
        player.note_off(note.number, volume)


def main(scale):
    cprint(scale, "blue")

    # initize Pygame MIDI ----------------------------------------------------------
    pygame.midi.init()
    # set the output device --------------------------------------------------------
    try:
        player = pygame.midi.Output(DEVICE)
    except:
        cprint("Device is not initialized", "red")
        pygame.midi.quit()
        return

    # set the instrument -----------------------------------------------------------
    player.set_instrument(INSTRUMENT)
    play(player, scale.notes)

    # close the device -------------------------------------------------------------
    del player
    pygame.midi.quit()


if __name__ == "__main__":
    main(HeptatonicScale("C", "major"))
    main(HeptatonicScale("C", "phrygian"))
    main(HeptatonicScale("C", "minor"))
    main(HeptatonicScale("C", "locrian"))

    main(HeptatonicScale("G", "major"))
    main(HeptatonicScale("G", "phrygian"))
    main(HeptatonicScale("G", "minor"))
    main(HeptatonicScale("G", "locrian"))
