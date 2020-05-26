import signal
import sys

from synth import Synth
from midi_file_player import MIDIFilePlayer
from termcolor import cprint


if sys.platform == "darwin":
    PORT_OUT = "FluidSynth"
else:
    PORT_OUT = "FLUID Synth"


synth = None


def signal_handler(sig, frame):
    global synth

    print("Shutting down.")
    synth.stop()
    sys.exit(0)


def main(path: str):
    global synth

    synth = Synth()
    synth.start()

    file = MIDIFilePlayer(synth, PORT_OUT)
    return file.play(path)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: mail_midi_player.py -l")
        print("       mail_midi_player.py <MIDI file>")

    signal.signal(signal.SIGINT, signal_handler)
    cprint("Press Ctrl+C to stop.", "yellow")

    if not main(sys.argv[1]):
        cprint("Cannot play the file. Exiting.", "red")
