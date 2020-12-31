from audio.input_device import SDInputDevice
from audio.tuner import Tuner

DEVICE = 5

# refer to the table of note frequencies when defining the tuner's range:
# https: // en.wikipedia.org / wiki / Piano_key_frequencies

GUITAR_TUNER_RANGE = (80, 340)    # allow detection from E2 to E4
UKULELE_TUNER_RANGE = (253, 453)  # allow detection from C4 to A4
OCT4_TUNER_RANGE = (253, 505)  # allow detection from C4 to B4

if __name__ == "__main__":
    print(SDInputDevice.available_devices())

    tuner = Tuner(device=DEVICE, freq_range=OCT4_TUNER_RANGE)
    tuner.start()
