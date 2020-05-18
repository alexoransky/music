import time
from pathlib import Path
import fluidsynth
import osascript

SOUND_FONT = "data/Nice-Keys-B-Plus-JN1.4.sf2"

FS_DRIVER = "coreaudio"
FS_MIDI_DRIVER = "coremidi"
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


class Synth:
    def __init__(self):
        self.fs = fluidsynth.Synth()
        self.sfid = None

    def start(self):
        self.fs.start(driver=FS_DRIVER, midi_driver=FS_MIDI_DRIVER, device=FS_DEVICE)

        self.fs.setting("synth.cpu-cores", FS_CPU_CORES)
        self.fs.setting("audio.period-size", FS_PERIOD_SIZE)
        self.fs.setting("synth.gain", FS_GAIN)

        self.sfid = self.fs.sfload(str(Path(SOUND_FONT).absolute().resolve()))
        self.fs.program_select(chan=FS_CHANNEL, sfid=self.sfid, bank=FS_BANK, preset=FS_PRESET)
        self.fs.cc(chan=FS_CHANNEL, ctrl=FS_CTRL_VOLUME, val=FS_VOLUME)

    def stop(self):
        # FluidSynth outputs some noise when the destructor is called
        # set system volume to 0 to avoid that
        code, prev_out, prev_err = osascript.run('output volume of (get volume settings)')
        cmd = "set volume output volume "
        code, out, err = osascript.run(cmd + "0")
        self.fs.delete()
        if prev_err is None or prev_err == "":
            code, out, err = osascript.run(cmd + prev_out)

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
