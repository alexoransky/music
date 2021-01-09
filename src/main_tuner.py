import math
from termcolor import cprint, colored
from audio.input_device import SDInputDevice
from audio.tuner import Tuner
from theory.notes import Note

DEVICE = 5

GUITAR_RANGE = ("E2", "E4")
UKULELE_TUNER_RANGE = ("C4", "A4")
F2_C5_RANGE = ("F2", "C5")

NF_WARNING_THRESHOLD = 0.6
NF_ERROR_THRESHOLD = 1.0


class CLITuner(Tuner):
    def __init__(self, note_range, note_a_freq_hz=440.0):
        self.freq_step = 0.2

        self.note_range = note_range
        self.midi_range = (Note.note_name_to_midi_number(note_range[0]), Note.note_name_to_midi_number(note_range[1]))

        self.tuner_note_range = self.get_tuner_range(note_range)
        f1, f2 = Tuner.get_freq_range(self.tuner_note_range, note_a_freq_hz)
        if f1 > 1000:
            self.freq_step = 0.5
        samples_per_frame = int(math.ceil(2*(f2-f1) / self.freq_step / 1024) * 1024)

        if Tuner.DEBUG_OUTPUT:
            cprint(f"Note A4 freq: {note_a_freq_hz:5.2f} Hz", "blue")
            cprint(f"Freq resolution: {self.freq_step:5.2f} Hz  Samples per frame: {samples_per_frame}", "blue")
        cprint("\rInitializing...", "yellow", end="")

        super().__init__(device=DEVICE, note_range=self.tuner_note_range,
                         freq_step=self.freq_step, samples_per_frame=samples_per_frame,
                         note_a_freq_hz=note_a_freq_hz)

    def get_tuner_range(self, init_note_range):
        midi_1 = Note.note_name_to_midi_number(init_note_range[0]) - 2
        midi_2 = Note.note_name_to_midi_number(init_note_range[1]) + 2
        n1 = Note.midi_number_to_note_name(midi_1, use_subscript=False)
        n2 = Note.midi_number_to_note_name(midi_2, use_subscript=False)
        return n1, n2

    def on_state_change(self):
        if self.data.noise_floor > NF_ERROR_THRESHOLD:
            cprint(f"\rToo noisy! NF={self.data.noise_floor:.2f}", "red")
        elif self.data.noise_floor > NF_WARNING_THRESHOLD:
            cprint(f"\rToo noisy! NF={self.data.noise_floor:.2f}", "yellow")
        print("\r                                        ", end="")

    def on_update(self):
        def error_str():
            if not Tuner.DEBUG_OUTPUT:
                return ""

            s = ""
            qsize = self.data.queue_size
            qerrors = self.errors.queue
            serrors = self.errors.sample

            if qsize > 1:
                s = f"Q:{qsize} "
            if qerrors > 0:
                s = f"Q:{qsize} QE:{qerrors} "

            if serrors > 0:
                s += f"SE:{serrors}"

            if len(s):
                s = "[" + s.rstrip() + "]"
                s = colored(s, "red")
            return s

        def note_str():
            f0, f1, f2 = Note.midi_number_to_freq_hz(self.data.midi_num)
            f1r = (f0 + f1) / 2
            f2r = (f0 + f2) / 2
            f1y = (f0 + f1r) / 2
            f2y = (f0 + f2r) / 2

            color = "green"
            if not (f1y < self.data.curr_freq < f2y):
                color = "yellow"
            if not (f1r < self.data.curr_freq < f2r):
                color = "red"

            s = f"{self.data.note} {self.data.delta_freq:+.2f} Hz"
            s = colored(s, color)

            if self.data.midi_num < self.midi_range[0]:
                color = "red"
                s = f"{self.note_range[0]}  Too low!"
                s = colored(s, color)

            if self.data.midi_num > self.midi_range[1]:
                color = "red"
                s = f"{self.note_range[1]}  Too high!"
                s = colored(s, color)

            return s

        if tuner.data.state == 1:
            print("\r                                                  ", end="")
            cprint(f"\r{note_str()}  [{self.data.curr_freq:7.2f} Hz]  {error_str()}", end="")


if __name__ == "__main__":
    # print(SDInputDevice.available_devices())
    # tuner = CLITuner(GUITAR_RANGE)
    tuner = CLITuner(UKULELE_TUNER_RANGE)
    tuner.start()
