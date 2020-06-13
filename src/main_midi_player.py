import signal
import sys
import time
from termcolor import cprint

from synth import Synth
from midi_file_player import MIDIFilePlayer, MIDIFile
from midi_metronome import MIDIMetronome


if sys.platform == "darwin":
    PORT_OUT = "FluidSynth"
else:
    PORT_OUT = "FLUID Synth"


synth = None
player = None
metronome = None
METRONOME = True
METRONOME_ONLY = False


def signal_handler(sig, frame):
    global synth
    global player
    global metronome

    print("Shutting down.")
    player.stop()
    metronome.stop()
    synth.stop()
    try:
        sys.exit(0)
    except:
        pass


def main(path: str):
    global synth
    global player
    global metronome

    synth = Synth()
    synth.start()

    player = MIDIFilePlayer(synth, PORT_OUT)
    metronome = MIDIMetronome(synth, PORT_OUT)

    if METRONOME_ONLY:
        metronome.start(210, 5)
        i = 0
        while metronome.is_playing:
            time.sleep(1)
            i += 1
            if i >= 8:
                break
        metronome.stop()
        ret = True
    else:
        # player.print(path)
        ret = player.open(path)

        player._file.print(notes=False)

        if METRONOME:
            metronome.velocity = 50
            metronome.start(210, 5)
        ret = player.play()
        # ret = player.play(start=135, end=182)
        # ret = player.play(start=15.0, end=20.0)
        i = 0
        while player.is_playing:
            time.sleep(1)
        #     i += 1
        #     if i >= 4:
        #         # player.pause()
        #         break
        #
        print(player.cursor)
        #
        # player.cursor = 296
        # print("Jump to: ", player.cursor)
        #
        # # player.cursor = 37.5
        # # print("Jump to: ", player.cursor)
        #
        # # player.pause(False)
        # while player.is_playing:
        #     time.sleep(1)

        player.stop()
        if METRONOME:
            metronome.stop()

    synth.stop()

    return ret


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: mail_midi_player.py -l")
        print("       mail_midi_player.py <MIDI file>")

    signal.signal(signal.SIGINT, signal_handler)
    cprint("Press Ctrl+C to stop.", "yellow")

    if not main(sys.argv[1]):
        cprint("Cannot play the file. Exiting.", "red")
