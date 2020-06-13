import sys
import time
from pathlib import Path
from dataclasses import dataclass
import fluidsynth

SOUND_FONT = "data/Nice-Keys-B-Plus-JN1.4.sf2"

if sys.platform == "darwin":
    FS_DRIVER = "coreaudio"
    FS_MIDI_DRIVER = "coremidi"
else:
    FS_DRIVER = "alsa"
    FS_MIDI_DRIVER = "alsa_seq"

FS_DEVICE = "default"

FS_CPU_CORES = 2
FS_PERIOD_SIZE = 256
FS_GAIN = 2.0
FS_VOLUME = 127
FS_VELOCITY = 64
FS_LENGTH = 0.6
FS_CHANNEL = 0
FS_BANK = 0
FS_PRESET = 0
FS_CTRL_VOLUME = 7
FS_STOP_DELAY_SEC = 1


class Synth:
    @dataclass
    class Channel:
        channel: int
        sound_font: object
        bank: int
        preset: int
        ctrl_volume: int
        volume: int

    def __init__(self):
        self.fs = fluidsynth.Synth()
        self.channels = {}

    def start(self):
        self.fs.start(driver=FS_DRIVER, midi_driver=FS_MIDI_DRIVER, device=FS_DEVICE)

        self.fs.setting("synth.cpu-cores", FS_CPU_CORES)
        self.fs.setting("audio.period-size", FS_PERIOD_SIZE)
        self.fs.setting("synth.gain", FS_GAIN)

        self.setup_channel(FS_CHANNEL, SOUND_FONT)

    def setup_channel(self, channel, sound_font_path,
                      bank=FS_BANK, preset=FS_PRESET, ctrl_volume=FS_CTRL_VOLUME, volume=FS_VOLUME):
        sound_font = self.fs.sfload(str(Path(sound_font_path).absolute().resolve()))
        self.fs.program_select(chan=channel, sfid=sound_font, bank=bank, preset=preset)
        self.fs.cc(chan=channel, ctrl=ctrl_volume, val=volume)

        ch = Synth.Channel(channel, sound_font, bank, preset, ctrl_volume, volume)
        self.channels[channel] = ch

    def stop(self, delay_sec=0):
        if delay_sec > 0:
            time.sleep(delay_sec)
        self.fs.delete()
        self.channels.clear()

    def play(self, notes, chord=False, velocity=FS_VELOCITY, wait=FS_LENGTH):
        if chord:
            for note in notes:
                self.fs.noteon(0, note.number, velocity)
            time.sleep(wait)
            for note in notes:
                self.fs.noteoff(0, note.number)
            return

        for note in notes:
            self.fs.noteon(0, note.number, velocity)
            time.sleep(wait)
            self.fs.noteoff(0, note.number)
