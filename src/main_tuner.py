from audio.input_device import SDInputDevice
from audio.tuner import Tuner

DEVICE = 5


if __name__ == "__main__":
    print(SDInputDevice.available_devices())

    tuner = Tuner(device=DEVICE)
    tuner.start()
