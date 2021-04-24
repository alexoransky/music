import math
from typing import Tuple, List
from termcolor import cprint, colored
from audio.input_device import SDInputDevice
from audio.tuner import Tuner
from theory.notes import Note

NF_WARNING_THRESHOLD = 0.6
NF_ERROR_THRESHOLD = 1.0

UKULELE_RANGE = ["C4", "A4"]
GUITAR_RANGE = ["E2", "D6"]
UKULELE_NOTES = ["G4", "C4", "E4", "A4"]
GUITAR_NOTES = ["E2", "A2", "D3", "G3", "B3", "E4"]
USE_FREQ_INDICATOR = False
DEBUG_OUTPUT = False


class CLTuner(Tuner):
    def __init__(self, device: int=None, note_range: Tuple[str, str]=None, note_list: List[str]=None, note_a_freq_hz: float=440.0):
        self.freq_step = 0.2
        self.note_range = note_range
        self.note_list = note_list
        self.midi_range = None
        self.midi_list = None

        # if no input device is supplied, try to find the default
        if device is None:
            device = SDInputDevice.default_device()
            if device is None:
                cprint("Cannot find input device!", "red")
                return
            else:
                cprint(f"Found input device: {device} {SDInputDevice.device_name(device)}", "yellow")
        else:
            cprint(f"Input device: {device} {SDInputDevice.device_name(device)}", "blue")

        # redefine the note range based on the supplied note list
        if self.note_list is not None:
            self.midi_list = self.note_names_to_midi_numbers(self.note_list)
            self.note_range = (Note.midi_number_to_note_name(self.midi_list[0], use_subscript=False),
                               Note.midi_number_to_note_name(self.midi_list[-1], use_subscript=False))

        self.midi_range = (Note.note_name_to_midi_number(self.note_range[0]),
                           Note.note_name_to_midi_number(self.note_range[1]))

        self.tuner_note_range = self.get_tuner_range(self.note_range)
        f1, f2 = Tuner.get_freq_range(self.tuner_note_range, note_a_freq_hz)
        if f2/f1 < 2.5:
            self.freq_step = 0.1
        if f1 > 1000:
            self.freq_step = 0.5
        samples_per_frame = int(math.ceil(2*(f2-f1) / self.freq_step / 1024) * 1024)

        if DEBUG_OUTPUT:
            cprint(f"Note A4 freq: {note_a_freq_hz:5.2f} Hz", "blue")
            cprint(f"Freq resolution: {self.freq_step:5.2f} Hz  Samples per frame: {samples_per_frame}", "blue")

        cprint(f"Tuner for range {Note.proper_note_name(self.note_range[0])} to {Note.proper_note_name(self.note_range[-1])}", "blue")
        # print(self.note_range)
        cprint("\rInitializing...", "yellow", end="")

        super().__init__(device=device, note_range=self.tuner_note_range,
                         freq_step=self.freq_step, samples_per_frame=samples_per_frame,
                         note_a_freq_hz=note_a_freq_hz)

    def get_tuner_range(self, init_note_range):
        midi_1 = Note.note_name_to_midi_number(init_note_range[0]) - 2
        midi_2 = Note.note_name_to_midi_number(init_note_range[1]) + 2
        n1 = Note.midi_number_to_note_name(midi_1, use_subscript=False)
        n2 = Note.midi_number_to_note_name(midi_2, use_subscript=False)
        return n1, n2

    def note_names_to_midi_numbers(self, note_names):
        midi = []
        for n in note_names:
            midi.append(Note.note_name_to_midi_number(n))
        return sorted(midi)

    def on_state_change(self):
        if self.data.noise_floor > NF_ERROR_THRESHOLD:
            cprint(f"\rToo noisy! NF={self.data.noise_floor:.2f}", "red")
        elif self.data.noise_floor > NF_WARNING_THRESHOLD:
            cprint(f"\rToo noisy! NF={self.data.noise_floor:.2f}", "yellow")
        print("\r                                        ", end="")

    def find_midi(self, freq):
        if self.note_list is None:
            return None

        curr_dist = 20000
        found = None
        for m in self.midi_list:
            f0, _, _ = Note.midi_number_to_freq_hz(m, note_a_freq_hz=self.note_a_freq_hz)
            dist = abs(f0-freq)
            if dist < curr_dist:
                found = m
                curr_dist = dist
        return found

    def on_update(self):
        def error_str():
            if not DEBUG_OUTPUT:
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

        def scale(fsd, curr, vc, minv, maxv):
            pos = round(fsd * (curr-vc) / (maxv - minv))
            pos = min(max(pos, -fsd), fsd)

            ticks = "╷" * (fsd-1)
            s = "│" + ticks + "│" + ticks + "│"
            idx = int(fsd + pos)
            ret = s[:idx] + "▼" + s[idx+1:]
            return ret

        def note_str():
            found_midi = self.find_midi(self.data.curr_freq)
            if found_midi is None:
                found_midi = self.data.midi_num
                found_note = self.data.note
            else:
                found_note = Note.midi_number_to_note_name(found_midi)

            f0, f1, f2 = Note.midi_number_to_freq_hz(found_midi)
            f1r = (f0 + f1) / 2
            f2r = (f0 + f2) / 2
            f1y = (f0 + f1r) / 2
            f2y = (f0 + f2r) / 2
            delta_freq = self.data.curr_freq - f0

            color = "green"
            if not (f1y < self.data.curr_freq < f2y):
                color = "yellow"
            if not (f1r < self.data.curr_freq < f2r):
                color = "red"

            if USE_FREQ_INDICATOR:
                s = f"{found_note} {delta_freq:+.2f} Hz"
            else:
                s = f"{found_note} {scale(10, self.data.curr_freq, f0, f1, f2)}"
            s = colored(s, color)
            s += f"  [{self.data.curr_freq:7.2f} Hz]"

            if self.note_list is None:
                if self.data.midi_num < self.midi_range[0]:
                    color = "red"
                    s = f"{self.note_range[0]}  Too low!"
                    s = colored(s, color)

                if self.data.midi_num > self.midi_range[1]:
                    color = "red"
                    s = f"{self.note_range[1]}  Too high!"
                    s = colored(s, color)

            return s

        print("\r                                                  ", end="")
        cprint(f"\r{note_str()}  {error_str()}", end="")


if __name__ == "__main__":
    # print(SDInputDevice.available_devices())
    tuner = CLTuner(5, note_range=UKULELE_RANGE)
    # tuner = CLTuner(note_list=UKULELE_NOTES)
    # tuner = CLTuner(note_range=GUITAR_RANGE)
    # tuner = CLTuner(note_list=GUITAR_NOTES)
    tuner.start()
