from time import sleep
import datetime
from bisect import bisect
from pathlib import Path
from threading import Thread
from dataclasses import dataclass
from mido import MidiFile, merge_tracks, tick2second, Message
from midi_router import MIDIRouter, MIDIPort


THREAD_PERIOD_MS = 50
DEFAULT_TEMPO = 500000
TRACE = True


class MIDIMessage:
    def __init__(self, msg: Message):
        self.msg = msg
        self.time_s: float = 0
        self.delta_s: float = 0
        self.duration_s: float = 0
        self.is_meta = msg.is_meta

    def __str__(self):
        return f"{round(self.time_s, 5)}: (+{round(self.delta_s, 5)}) [{round(self.duration_s, 5)}] {self.msg}"


class MIDIFile(MidiFile):
    def __init__(self, path: str):
        self.path = self.absolute_path(path)
        super().__init__(self.path, clip=True)

        self.messages = None
        self.time_marks = None
        self.tempo = DEFAULT_TEMPO

        # merge tracks for simple playback if the file is not asynchronous
        if self.type != 2:
            self.messages, self.time_marks = self._calculate_time(merge_tracks(self.tracks))

    def _calculate_time(self, msgs):
        messages = []
        time_marks = []
        self.tempo = DEFAULT_TEMPO
        mark = 0
        notes = {}
        for idx, msg in enumerate(msgs):
            if msg.type == 'set_tempo':
                self.tempo = msg.tempo
            delta = tick2second(msg.time, self.ticks_per_beat, self.tempo)
            mark += delta

            time_marks.append(mark)

            if msg.type == "note_on" and msg.velocity > 0:
                notes[msg.note] = idx
            if msg.type == "note_off" or \
               msg.type == "note_on" and msg.velocity == 0:
                i = notes.get(msg.note, None)
                if i is not None:
                    messages[i].duration_s = mark - messages[i].time_s

            message = MIDIMessage(msg)
            message.delta_s = delta
            message.time_s = mark
            messages.append(message)
        return messages, time_marks

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

    def time_mark_to_msg_index(self, mark):
        return bisect(self.time_marks, mark)

    def msg_index_to_time_mark(self, idx):
        if 0 <= idx < len(self.time_marks):
            return self.time_marks[idx]
        elif idx < 0:
            return self.time_marks[0]
        else:
            return self.time_marks[-1]

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

        if self.type == 2:
            for idx, track in enumerate(self.tracks):
                self.print_track(idx, meta=meta, notes=notes)
        else:
            for idx, msg in enumerate(self.messages):
                if meta and msg.msg.is_meta or \
                   notes and not msg.msg.is_meta:
                    print(idx, ":", round(msg.time_s, 4), ":", msg.msg)

        print()


class MIDIFilePlayer:
    @dataclass()
    class Mark:
        idx: int = 0
        time: float = 0

        def reset(self):
            self.idx = 0
            self.time = 0

        def __str__(self):
            return "[" + str(self.idx) + " " + str(round(self.time, 6)) + "]"

    class State:
        STOPPED = 0
        PLAYING = 1
        PAUSING = 2
        PAUSED = 3

    def __init__(self, synth, port_mask):
        self._synth = synth
        self._port_mask = port_mask
        self._file = None
        self._ports = None

        self._cursor = MIDIFilePlayer.Mark()
        self._start = MIDIFilePlayer.Mark()
        self._end = MIDIFilePlayer.Mark()
        self._total_message_cnt = 0

        self._active = False
        self._thread = None
        self._thread_period = THREAD_PERIOD_MS * 0.001
        self._state = MIDIFilePlayer.State.STOPPED

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

    def _play(self):
        port_cnt = len(self._ports)
        curr_notes = set()
        while self._active:
            if self._state == MIDIFilePlayer.State.PAUSED:
                sleep(self._thread_period)
                continue

            if self._cursor.idx >= self._total_message_cnt or \
               self._cursor.idx >= self._end.idx:
                self._state = MIDIFilePlayer.State.PAUSING

            if self._state == MIDIFilePlayer.State.PAUSING:
                if len(curr_notes) == 0:
                    self._state = MIDIFilePlayer.State.PAUSED
                    continue

            message = self._file.messages[self._cursor.idx]
            if TRACE:
                print("Read msg:", self._cursor, ":", message, flush=True)

            sleep(message.delta_s)
            self._cursor.time += message.delta_s
            self._cursor.idx += 1

            msg = message.msg
            if msg.is_meta:
                continue

            if msg.channel >= port_cnt:
                msg.channel = port_cnt - 1

            try:
                if self._state == MIDIFilePlayer.State.PAUSING:
                    if msg.type == "note_on" and msg.velocity > 0:
                        continue

                self._ports[msg.channel].send(msg)
                if TRACE:
                    print("Sent msg: ", msg, flush=True)

                if msg.type == "note_on" and msg.velocity > 0:
                    curr_notes.add((msg.channel, msg.note))
                if msg.type == "note_off" or \
                   msg.type == "note_on" and msg.velocity == 0:
                    curr_notes.remove((msg.channel, msg.note))
            except:
                pass

    def open(self, path: str):
        self._file = MIDIFile(path)
        self._total_message_cnt = len(self._file.messages)

    def close(self):
        self._file = None
        self._cursor.reset()
        self._start.reset()
        self._end.reset()
        self._total_message_cnt = 0

    def play(self, start=None, end=None, max_channel_cnt=1):
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

        self._cursor.reset()
        if self._total_message_cnt == 0:
            return False

        self.start = start
        self.end = end
        self._cursor = self._start

        self._thread = Thread(target=self._play)
        self._active = True
        self._state = MIDIFilePlayer.State.PLAYING
        self._thread.start()

        return True

    def stop(self):
        self._active = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        self._close_ports()
        self._thread = None
        self._state = MIDIFilePlayer.State.STOPPED
        self._cursor.reset()
        self._start.reset()
        self._end.reset()

    def pause(self, pause=True):
        if pause:
            # finish playing current notes, then pause
            self._state = MIDIFilePlayer.State.PAUSING
        else:
            # move the time mark to the beginning of the note, then release
            self._cursor.time -= self._file.messages[self._cursor.idx].delta_s
            self._state = MIDIFilePlayer.State.PLAYING

    @property
    def is_active(self):
        return self._active

    @property
    def is_playing(self):
        return self._state == MIDIFilePlayer.State.PLAYING

    @property
    def total_msg_cnt(self):
        return self._total_message_cnt

    @property
    def length(self):
        return self._file.length

    @property
    def cursor(self):
        return self._cursor.idx, self._cursor.time

    @cursor.setter
    def cursor(self, mark):
        state = self._state
        if self._state == MIDIFilePlayer.State.PLAYING:
            self._state = MIDIFilePlayer.State.PAUSING
        while self._state != MIDIFilePlayer.State.PAUSED:
            sleep(THREAD_PERIOD_MS/10)

        if isinstance(mark, int):
            self._cursor.time = self._file.msg_index_to_time_mark(mark)
            self._cursor.idx = mark
        elif isinstance(mark, float):
            self._cursor.idx = self._file.time_mark_to_msg_index(mark)
            self._cursor.time = self._file.msg_index_to_time_mark(self._cursor.idx)

        if state == MIDIFilePlayer.State.PLAYING:
            self._state = MIDIFilePlayer.State.PLAYING

    @property
    def start(self):
        return self._start.idx, self._start.time

    @start.setter
    def start(self, mark):
        self._start.reset()
        if mark is None:
            return

        if isinstance(mark, int):
            idx = mark
        elif isinstance(mark, float):
            idx = self._file.time_mark_to_msg_index(mark)
        else:
            return

        self._start.idx = idx
        self._start.time = self._file.msg_index_to_time_mark(idx) - self._file.messages[idx].delta_s

    @property
    def end(self):
        return self._end.idx, self._end.time

    @end.setter
    def end(self, mark):
        self._end.idx = self._total_message_cnt
        self._end.time = self._file.length

        if mark is None:
            return

        if isinstance(mark, int):
            if 0 <= mark < self._total_message_cnt:
                self._end.idx = mark
                self._end.time = self._file.msg_index_to_time_mark(mark)
        elif isinstance(mark, float):
            if 0 <= mark < self._file.length:
                self._end.idx = self._file.time_mark_to_msg_index(mark)
                self._end.time = self._file.msg_index_to_time_mark(self._end.idx)
