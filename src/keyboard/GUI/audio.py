from threading import Thread

from synth import Synth
from midi_router import MIDIRouter
from midi_parser import MIDIParser
from tuning import Tuning


class AudioSupport:
    def __init__(self):
        self.sf = None
        self.midi_in = None
        self.midi_out = None

        self.synth = None
        self.midi_router = None
        self.is_active = False
        self.parser = None
        self.parser_thread = Thread(target=self._parse_midi_events)

    @classmethod
    def available_midi_ports(cls):
        synth = Synth()
        synth.start()

        # find input and output MIDI ports
        in_ports = MIDIRouter.available_ports(output=False)
        out_ports = MIDIRouter.available_ports(output=True)

        synth.stop()

        return in_ports, out_ports

    def start_midi(self, port_in, port_out, sound_font_path=None, bank=None, preset=None, start_parser=True):
        self.synth = Synth()
        self.synth.start()
        self.synth.tune(0, 432, tuning=Tuning.TUNING_5_LIMIT)

        # alternative sound font
        if sound_font_path is not None:
            self.sf = sound_font_path
            self.synth.setup_channel(channel=0, sound_font_path=sound_font_path, bank=bank, preset=preset)

        # find input and output MIDI ports
        try:
            in_ports = MIDIRouter.available_ports(output=False)
            out_ports = MIDIRouter.available_ports(output=True)
        except:
            return False

        _port_in = None
        _port_out = None
        for port in in_ports:
            if port_in in port:
                _port_in = port
                break

        for port in out_ports:
            if port_out in port:
                _port_out = port
                break

        self.midi_router = MIDIRouter(port_in=_port_in, port_out=_port_out, message_filter=["aftertouch"])
        ret = self.midi_router.start()

        if ret and start_parser:
            self.start_midi_parser()

        return ret

    def stop_midi(self):
        if self.is_active:
            self.stop_midi_parser()
        self.midi_router.stop()
        self.synth.stop()

    def _parse_midi_events(self):
        self.parser = MIDIParser()

        while self.is_active:
            self.parser.parse(self.midi_router.get_message())

    def start_midi_parser(self):
        if self.is_active:
            return

        self.is_active = True
        self.parser_thread.start()

    def stop_midi_parser(self):
        if not self.is_active:
            return

        self.is_active = False
        self.parser_thread.join()
