import signal
import sys
import time

from synth import Synth
from midi_file_player import MIDIFilePlayer
from termcolor import cprint


if sys.platform == "darwin":
    PORT_OUT = "FluidSynth"
else:
    PORT_OUT = "FLUID Synth"


synth = None
player = None


def signal_handler(sig, frame):
    global synth

    print("Shutting down.")
    player.stop()
    synth.stop()
    try:
        sys.exit(0)
    except:
        pass


def main(path: str):
    global synth
    global player

    synth = Synth()
    synth.start()

    player = MIDIFilePlayer(synth, PORT_OUT)
    # player.print(path)
    ret = player.open(path)

    i = 0
    ret = player.start()
    while player.is_active and not player.is_paused:
        time.sleep(1)
        i += 1
        if i >= 3:
            player.pause()
            break

    time.sleep(3)
    player.pause(False)
    while player.is_active and not player.is_paused:
        time.sleep(1)

    player.stop()

    return ret


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: mail_midi_player.py -l")
        print("       mail_midi_player.py <MIDI file>")

    signal.signal(signal.SIGINT, signal_handler)
    cprint("Press Ctrl+C to stop.", "yellow")

    if not main(sys.argv[1]):
        cprint("Cannot play the file. Exiting.", "red")
