import signal
import sys

from pprint import pprint
from termcolor import cprint

from audio import Synth, MIDIRouter, MIDIParser, Tuning

PORT_IN = "Arturia"
if sys.platform == "darwin":
    PORT_OUT = "FluidSynth"
else:
    PORT_OUT = "FLUID Synth"

CHANNEL = 0
NOTE_A_FREQ = 440
TUNING = Tuning.TUNING_12_TET
# TUNING = Tuning.TUNING_5_LIMIT

# Alternative sound font, bank and preset
#SOUND_FONT = "../data/OmegaGMGS2.sf2"
#
# Stereo Standart
# SF_BANK = 128
# SF_PRESET = 4
#
# SFX
# SF_BANK = 128
# SF_PRESET = 56
#
# Sine Wave XG
# SF_BANK = 66
# SF_PRESET = 80


SOUND_FONT = "../data/20-synth-sf/Perfect Sine.sf2"
# SOUND_FONT = "../data/Sine Wave.sf2"
SF_BANK = 0
SF_PRESET = 0

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
    try:
        in_ports = MIDIRouter.available_ports(output=False)
        out_ports = MIDIRouter.available_ports(output=True)
    except:
        return False

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

    midi_router = MIDIRouter(port_in=port_in, port_out=port_out, message_filter=["aftertouch"])
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
    synth.tune(CHANNEL, NOTE_A_FREQ, tuning=TUNING)
    # alternative sound font
    synth.setup_channel(channel=0, sound_font_path=SOUND_FONT, bank=SF_BANK, preset=SF_PRESET)

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
        cprint("Cannot find the required MIDI ports. Exiting.", "red")
