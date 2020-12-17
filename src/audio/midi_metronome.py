from time import sleep
from threading import Thread
from mido import Message

from .midi_router import MIDIRouter, MIDIPort


THREAD_PERIOD_MS = 50
DEFAULT_TEMPO = 120
DEFAULT_MESURE_LEN = 4
TRACE = True

SOUND_FONT = "data/OmegaGMGS2.sf2"
FS_CHANNEL = 10
SF_BANK = 128
SF_PRESET = 56
CLICK = 45
BELL = 46  # 44
# SF_PRESET = 4
# CLICK = 33
# BELL = 32  # 62
DEFAULT_VELOCITY = 90
DEFAULT_BELL_VELOCITY_DELTA = 20
DEFAULT_LEN = 0.001


class MIDIMetronome:
    class State:
        STOPPED = 0
        PLAYING = 1
        PAUSED = 2

    def __init__(self, synth, port_mask):
        self._synth = synth
        self._port = self._open_port(port_mask)
        self._channel = FS_CHANNEL

        self._active = False
        self._thread = None
        self._thread_period = THREAD_PERIOD_MS * 0.001
        self._state = MIDIMetronome.State.STOPPED

        self._tempo = DEFAULT_TEMPO
        self._measure_len = DEFAULT_MESURE_LEN
        self._note_len = DEFAULT_LEN
        self._velocity = DEFAULT_VELOCITY
        self._use_bell = True

        self.click = None
        self.bell = None

        self._synth.setup_channel(self._channel, SOUND_FONT, SF_BANK, SF_PRESET)

    def _open_port(self, port_mask):
        port = None
        out_ports = MIDIRouter.available_ports(output=True)
        for port_name in out_ports:
            if port_mask in port_name:
                port = MIDIPort()
                port.open(port_name)
                if port.is_open():
                    break
        return port

    def _play(self):
        cnt = 0
        while self._active:
            if self._state == MIDIMetronome.State.PAUSED:
                sleep(self._thread_period)
                continue

            if self._use_bell and cnt == 0:
                msg = self.bell
                msg.velocity = min(127, self._velocity+DEFAULT_BELL_VELOCITY_DELTA)
            else:
                msg = self.click
                msg.velocity = self._velocity

            self._port.send(msg)
            sleep(self._note_len)

            msg.velocity = 0
            self._port.send(msg)
            delta_s = 60 / self._tempo
            sleep(delta_s - self._note_len)

            cnt += 1
            if cnt >= self._measure_len:
                cnt = 0

    def start(self, tempo=None, measure_len=None):
        if not self._port.is_open():
            return False

        if tempo is not None:
            self._tempo = tempo
        if measure_len is not None:
            self._measure_len = measure_len

        self.click = Message("note_on", note=CLICK, velocity=self._velocity, time=self._note_len, channel=self._channel)
        self.bell = Message("note_on", note=BELL, velocity=self._velocity, time=self._note_len, channel=self._channel)

        self._thread = Thread(target=self._play)
        self._active = True
        self._state = MIDIMetronome.State.PLAYING
        self._thread.start()

        return True

    def stop(self):
        self._active = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        self._thread = None
        self._state = MIDIMetronome.State.STOPPED

    def pause(self, pause=True):
        # TODO: set the next note to BELL when the metronome is released
        if pause:
            self._state = MIDIMetronome.State.PAUSED
        else:
            self._state = MIDIMetronome.State.PLAYING

    @property
    def is_active(self):
        return self._active

    @property
    def is_playing(self):
        return self._state == MIDIMetronome.State.PLAYING

    @property
    def measure_len(self):
        return self._measure_len

    @measure_len.setter
    def measure_len(self, value):
        self._measure_len = value

    @property
    def tempo(self):
        return self._tempo

    @tempo.setter
    def tempo(self, value):
        self._tempo = value

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = value
