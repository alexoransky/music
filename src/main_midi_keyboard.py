import signal
import sys

from synth import Synth
from midi_router import MIDIRouter
from midi_parser import MIDIParser
from termcolor import cprint


PORT_IN = "Arturia"
PORT_OUT = "FluidSynth"


synth = None
midi_router = None


def signal_handler(sig, frame):
    global synth
    global midi_router

    print("Shutting down.")
    midi_router.stop()
    synth.stop()
    sys.exit(0)


def init_midi_router():
    global midi_router

    # find input and output MIDI ports
    in_ports = MIDIRouter.available_ports(output=False)
    out_ports = MIDIRouter.available_ports(output=True)

    port_in = None
    port_out = None
    for port in in_ports:
        if PORT_IN in port:
            port_in = port

    for port in out_ports:
        if PORT_OUT in port:
            port_out = port

    midi_router = MIDIRouter(port_in=port_in, port_out=port_out)
    return midi_router.start()


def main():
    global synth
    global midi_router

    synth = Synth()
    synth.start()

    if not init_midi_router():
        return False

    parser = MIDIParser()

    while True:
        parser.parse(midi_router.get_message())


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    cprint("Press Ctrl+C to stop.", "yellow")

    if not main():
        cprint("Cannot find the required ports. Exiting.", "red")
