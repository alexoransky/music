from pathlib import Path
from mido import MidiFile
from midi_router import MIDIRouter, MIDIPort


class MIDIFilePlayer:
    def __init__(self, synth, port_mask):
        self.synth = synth
        self.port_mask = port_mask
        self.ports = []

    def _open_ports(self, max_count: int = 0):
        self.ports.clear()
        out_ports = MIDIRouter.available_ports(output=True)
        cnt = 0
        for port_name in out_ports:
            if self.port_mask in port_name:
                port = MIDIPort()
                port.open(port_name)
                if not port.is_open():
                    return False

                self.ports.append(port)
                cnt += 1
            if max_count > 0:
                if cnt >= max_count:
                    break

        if cnt == 0 or cnt < max_count:
            return False

        return True

    def _close_ports(self):
        for port in self.ports:
            port.close()
        self.ports.clear()

    def play(self, path: str, max_channel_cnt=1):
        file = MidiFile(str(Path(path).absolute().resolve()))

        port_cnt = min(len(file.tracks), max_channel_cnt)
        if port_cnt == 0:
            port_cnt = 1

        if not self._open_ports(max_count=port_cnt):
            return False

        for ch in range(port_cnt):
            self.synth.setup_channel(ch)

        for msg in file.play():
            if msg.channel >= port_cnt:
                msg.channel = port_cnt - 1
            self.ports[msg.channel].send(msg)

        self._close_ports()
        return True

    def print(self, path: str, meta=True, notes=False):
        file = MidiFile(str(Path(path).absolute().resolve()))

        for i, track in enumerate(file.tracks):
            print('Track {}: {}'.format(i, track.name))
            for msg in track:
                if meta and msg.is_meta:
                    print(msg)
                    continue
                if notes and not msg.is_meta:
                    print(msg)

    def stop(self):
        self._close_ports()
