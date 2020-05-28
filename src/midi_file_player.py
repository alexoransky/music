import time
from pathlib import Path
from threading import Thread
from mido import MidiFile
from midi_router import MIDIRouter, MIDIPort


class MIDIFile(MidiFile):
    def __init__(self, path: str):
        self.path = str(Path(path).absolute().resolve())
        super().__init__(self.path, clip=True)
        self.total_msg_cnt = self._get_total_message_count()

    def _get_total_message_count(self, include_meta=False):
        cnt = 0
        for track in self.tracks:
            for msg in track:
                if msg.is_meta and not include_meta:
                    continue
                cnt += 1
        return cnt


class MIDIFilePlayer:
    def __init__(self, synth, port_mask):
        self._synth = synth
        self._port_mask = port_mask
        self._file = None
        self._ports = []
        self._active = False
        self._paused = False
        self._curr_msg_cnt = 0
        self._thread = None
        self._thread_period_ms = 50

    def _open_ports(self, max_count: int = 0):
        self._ports.clear()
        out_ports = MIDIRouter.available_ports(output=True)
        cnt = 0
        for port_name in out_ports:
            if self._port_mask in port_name:
                port = MIDIPort()
                port.open(port_name)
                if not port.is_open():
                    return False

                self._ports.append(port)
                cnt += 1
            if max_count > 0:
                if cnt >= max_count:
                    break

        if cnt == 0 or cnt < max_count:
            return False

        if len(self._ports) < 1:
            return False

        return True

    def _close_ports(self):
        for port in self._ports:
            port.close()
        self._ports.clear()

    def open(self, path: str):
        self._file = MIDIFile(path)

    def close(self):
        self._file = None

    def start(self, max_channel_cnt=1):
        port_cnt = min(len(self._file.tracks), max_channel_cnt)
        if port_cnt == 0:
            port_cnt = 1

        if not self._open_ports(max_count=port_cnt):
            return False

        for ch in range(port_cnt):
            self._synth.setup_channel(ch)

        self._thread = Thread(target=self._play)
        self._active = True
        self._curr_msg_cnt = 0
        self._thread.start()

        return True

    def _play(self):
        port_cnt = len(self._ports)
        msgs = self._file.play()
        while self._active:
            if self._paused:
                time.sleep(self._thread_period_ms * 0.001)
                continue
            try:
                msg = next(msgs)
            except:
                self._active = False
                return

            if msg.channel >= port_cnt:
                msg.channel = port_cnt - 1

            self._curr_msg_cnt += 1
            self._ports[msg.channel].send(msg)

    def stop(self):
        self._active = False
        if self._thread is not None:
            self._thread.join()
        self._close_ports()
        self._thread = None
        self._paused = False
        self._curr_msg_cnt = 0

    def pause(self):
        self._paused = True

    def release(self):
        self._paused = False

    def is_playing(self):
        return self._active

    def is_paused(self):
        return self._paused

    def total_msg_cnt(self):
        return self._file.total_msg_cnt

    def curr_msg_cnt(self):
        return self._curr_msg_cnt

    def duration(self):
        return self._file.length()

    @classmethod
    def print(cls, path: str, meta=True, notes=False):
        file = MidiFile(str(Path(path).absolute().resolve()))

        print(file)
        for i, track in enumerate(file.tracks):
            print('Track {}: {}'.format(i, track.name))
            for msg in track:
                if meta and msg.is_meta:
                    print(msg)
                    continue
                if notes and not msg.is_meta:
                    print(msg)
