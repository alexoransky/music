from audio.input_device import SDInputDevice
from audio.tuner import Tuner

DEVICE = 5

# refer to the table of note frequencies when defining the tuner's range:
# https: // en.wikipedia.org / wiki / Piano_key_frequencies

GUITAR_TUNER_RANGE = (80, 340)    # allow detection from E2 to E4
UKULELE_TUNER_RANGE = (253, 453)  # allow detection from C4 to A4
OCT4_TUNER_RANGE = (253, 505)     # allow detection from C4 to B4
F2_C5_TUNER_RANGE = (84, 539)     # allow detection from F2 to C5

if __name__ == "__main__":
    print(SDInputDevice.available_devices())

    tuner = Tuner(device=DEVICE, freq_range=F2_C5_TUNER_RANGE, freq_step=1.0)
    tuner.start()
