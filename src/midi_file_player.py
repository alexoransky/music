import time
import datetime
from pathlib import Path
from threading import Thread
from mido import MidiFile, merge_tracks, tick2second
from midi_router import MIDIRouter, MIDIPort


THREAD_PERIOD_MS = 50
DEFAULT_TEMPO = 500000
TRACE = False


class MIDIFile(MidiFile):
    def __init__(self, path: str):
        self.path = self.absolute_path(path)
        super().__init__(self.path, clip=True)

        self.messages = None

        # merge tracks for simple playback if the file is not asynchronous
        if self.type != 2:
            self.messages = merge_tracks(self.tracks)

    def track_count(self, playable_only=True):
        cnt = 0
        for track in self.tracks:
            if self.track_message_count(track, include_meta=not playable_only) > 0:
                cnt += 1
        return cnt

    def track_message_count(self, track, include_meta=False):
        cnt = 0
        for msg in track:
            if msg.is_meta and not include_meta:
                continue
            cnt += 1
        return cnt

    def message_count(self, include_meta=False, merged=True):
        cnt = 0
        if merged:
            if self.type != 2:
                cnt += self.track_message_count(self.messages, include_meta=include_meta)
            return cnt

        for track in self.tracks:
            cnt += self.track_message_count(track, include_meta=include_meta)
        return cnt

    @classmethod
    def absolute_path(cls, path: str):
        abs_path = str(Path(path).absolute().resolve())
        return abs_path

    def print_track(self, idx, meta=True, notes=False):
        track = self.tracks[idx]
        print('Track {}: {}'.format(idx, track.name))
        for msg in track:
            if meta and msg.is_meta:
                print(msg)
                continue
            if notes and not msg.is_meta:
                print(msg)
        print()

    def print(self, meta=True, notes=False):
        if meta:
            print("File:", self.path)
            print("Type:", self.type)
            print("Tracks:", len(self.tracks), "Playable:", self.track_count(playable_only=True))
            print("Total messages:", self.message_count(include_meta=True, merged=False),
                  "Merged:", self.message_count(include_meta=True, merged=True),
                  "Playable:", self.message_count(include_meta=False))
            print("Total time:", datetime.timedelta(seconds=round(self.length)))
            print()

        for idx, track in enumerate(self.tracks):
            self.print_track(idx, meta=meta, notes=notes)


class MIDIFilePlayer:
    def __init__(self, synth, port_mask):
        self._synth = synth
        self._port_mask = port_mask
        self._file = None
        self._ports = None

        self._curr_time_mark = 0
        self._curr_message_idx = 0
        self._total_message_cnt = 0
        self._tempo = DEFAULT_TEMPO

        self._active = False
        self._paused = False
        self._thread = None
        self._thread_period = THREAD_PERIOD_MS * 0.001

    def _open_ports(self, max_count: int = 0):
        """
        Tries to open the requested number of ports
        :param max_count: the requested number of ports to open.  If 0, tries to open all
        :return: a list of opened ports
        """
        ports = []
        out_ports = MIDIRouter.available_ports(output=True)
        for port_name in out_ports:
            if self._port_mask in port_name:
                port = MIDIPort()
                port.open(port_name)
                if not port.is_open():
                    continue

                ports.append(port)

            if max_count > 0:
                if len(ports) >= max_count:
                    break

        return ports

    def _close_ports(self):
        for port in self._ports:
            port.close()
        self._ports.clear()

    def _time_s(self, msg_idx):
        delta = 0
        if 0 <= msg_idx < self._total_message_cnt:
            ticks = self._file.messages[msg_idx].time
            if ticks == 0:
                return 0
            delta = tick2second(ticks, self._file.ticks_per_beat, self._tempo)
        return delta

    def _play(self):
        port_cnt = len(self._ports)
        self._tempo = DEFAULT_TEMPO
        while self._active:
            if self._paused:
                time.sleep(self._thread_period)
                continue

            if self._curr_message_idx >= self._total_message_cnt:
                self._paused = True
                continue

            msg = self._file.messages[self._curr_message_idx]

            if msg.type == 'set_tempo':
                self._tempo = msg.tempo

            delta = self._time_s(self._curr_message_idx)
            time.sleep(delta)
            self._curr_time_mark += delta
            if TRACE:
                print(self._curr_message_idx, ": ", self._curr_time_mark, ": ", msg, flush=True)
            self._curr_message_idx += 1

            if msg.is_meta:
                continue

            if msg.channel >= port_cnt:
                msg.channel = port_cnt - 1
            try:
                self._ports[msg.channel].send(msg)
            except:
                pass

    def _time_mark_to_msg_index(self, value):
        self._tempo = DEFAULT_TEMPO
        mark = 0
        for idx, msg in enumerate(self._file.messages):
            if msg.type == 'set_tempo':
                self._tempo = msg.tempo
            mark += self._time_s(idx)
            if mark >= value:
                return idx
        return len(self._file.messages)

    def _msg_index_to_time_mark(self, value):
        self._tempo = DEFAULT_TEMPO
        mark = 0
        for idx, msg in enumerate(self._file.messages):
            if msg.type == 'set_tempo':
                self._tempo = msg.tempo
            mark += self._time_s(idx)
            if value <= idx:
                return mark
        return mark

    def open(self, path: str):
        self._file = MIDIFile(path)

    def close(self):
        self._file = None
        self._curr_message_idx = 0
        self._total_message_cnt = 0

    def start(self, max_channel_cnt=1):
        port_cnt = self._file.track_count(playable_only=True)
        if port_cnt < 1:
            return False

        port_cnt = min(port_cnt, max_channel_cnt)
        if port_cnt == 0:
            port_cnt = 1

        self._ports = self._open_ports(port_cnt)
        if len(self._ports) == 0:
            return False

        for ch in range(port_cnt):
            self._synth.setup_channel(ch)

        self._curr_message_idx = 0
        self._total_message_cnt = len(self._file.messages)
        if self._total_message_cnt == 0:
            return False

        self._thread = Thread(target=self._play)
        self._active = True
        self._paused = False
        self._thread.start()

        return True

    def stop(self):
        self._active = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        self._close_ports()
        self._thread = None
        self._paused = False
        self._curr_message_idx = 0

    def pause(self, pause=True):
        def time_s():
            delta = 0
            idx = self._curr_message_idx
            while 0 <= idx < self._total_message_cnt and idx - self._curr_message_idx < 20:
                delta = self._time_s(idx)
                if delta > 0:
                    break
                idx += 1
            return delta

        if pause:
            # finish playing the current note, then pause
            self._paused = True
            time.sleep(time_s())
        else:
            # move the time mark to the beginning of the note, then release
            self._curr_time_mark -= self._time_s(self._curr_message_idx)
            self._paused = False

    @property
    def is_active(self):
        return self._active

    @property
    def is_paused(self):
        return self._paused

    @property
    def total_msg_cnt(self):
        return self._total_message_cnt

    @property
    def curr_msg_idx(self):
        return self._curr_message_idx

    @curr_msg_idx.setter
    def curr_msg_idx(self, value):
        paused = self._paused
        if not paused:
            self.pause(True)

        self._curr_time_mark = self._msg_index_to_time_mark(value)
        self._curr_message_idx = value

        if not paused:
            self.pause(False)

    @property
    def length(self):
        return self._file.length

    @property
    def time_mark(self):
        return self._curr_time_mark

    @time_mark.setter
    def time_mark(self, value):
        paused = self._paused
        if not paused:
            self.pause(True)

        self._curr_message_idx = self._time_mark_to_msg_index(value)
        self._curr_time_mark = self._msg_index_to_time_mark(self._curr_message_idx)

        if not paused:
            self.pause(False)
