import signal
import sys

from pprint import pprint

from synth import Synth
from midi_router import MIDIRouter
from midi_parser import MIDIParser
from termcolor import cprint


PORT_IN = "Arturia"

if sys.platform == "darwin":
    PORT_OUT = "FluidSynth"
else:
    PORT_OUT = "FLUID Synth"


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
            break

    for port in out_ports:
        if PORT_OUT in port:
            port_out = port
            break

    midi_router = MIDIRouter(port_in=port_in, port_out=port_out)
    return midi_router.start()


def list_ports():
    global synth

    synth = Synth()
    synth.start()

    # find input and output MIDI ports
    in_ports = MIDIRouter.available_ports(output=False)
    out_ports = MIDIRouter.available_ports(output=True)

    cprint("Input MIDI ports:", "blue")
    pprint(in_ports)
    cprint("Output MIDI ports:", "blue")
    pprint(out_ports)

    synth.stop()


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
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "-l":
            list_ports()
            sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    cprint("Press Ctrl+C to stop.", "yellow")

    if not main():
        cprint("Cannot find the required ports. Exiting.", "red")
