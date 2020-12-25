from threading import Thread
from fifo_queue import FIFOQueue
from time import sleep

import sounddevice as sd
import pyaudio


# PortAudio has a bug that does not let setting varios sample rates
DEFAULT_SAMPLE_RATE = 48000


class InputDevice:
    def __init__(self, device, channel_cnt: int, samples_per_frame: int, queue_data: bool, max_queue_len: int):
        self._device = device
        self._sample_rate = DEFAULT_SAMPLE_RATE

        self._channel_cnt = channel_cnt
        self._active = False
        self._thread = None

        self._samples_per_frame = samples_per_frame

        # data will either be queued or processed by the supplied process function
        self._process_fn = None
        self._queue = None
        if queue_data:
            self._queue = FIFOQueue(max_len=max_queue_len)

    @classmethod
    def available_devices(cls):
        return "No devices available. Use SDInputDevice or PAInputDevice class instead."

    def set_device(self, device):
        self._device = device

    def set_sample_rate(self, samples_per_s):
        self._sample_rate = samples_per_s

    def get_sample_rate(self):
        return self._sample_rate

    def set_samples_per_frame(self, samples_per_frame):
        self._samples_per_frame = samples_per_frame

    def set_channel_cnt(self, cnt):
        self._channel_cnt = cnt

    def set_process_fn(self, process_fn):
        self._process_fn = process_fn

    def start(self):
        self._active = True
        self._thread = Thread(target=self._main_loop)
        self._thread.start()

    def stop(self):
        self._active = False
        self._thread.join()

    def get_data(self):
        if self._queue is None:
            return None
        return self._queue.get()

    def queue_size(self):
        if self._queue is None:
            return None
        return self._queue.size()

    def _callback_fn(self, indata, frames, time, status):
        if self._queue is not None:
            self._queue.put(indata)

        if self._process_fn is not None:
            self._process_fn(indata)

    def _main_loop(self):
        if not self._active:
            return
        # implement the receive loop here


class SDInputDevice(InputDevice):
    def __init__(self, device=None, channel_cnt=1, samples_per_frame=2048, queue_data=True, max_queue_len=200):
        super(SDInputDevice, self).__init__(device=device,
                                            channel_cnt=channel_cnt,
                                            samples_per_frame=samples_per_frame,
                                            queue_data=queue_data,
                                            max_queue_len=max_queue_len)

        if device is not None:
            self.set_device(device)

        # data will either be queued or processed by the supplied function
        # data is formatted as specified in the callback section:
        # https://python-sounddevice.readthedocs.io/en/0.4.1/api/streams.html

    @classmethod
    def available_devices(cls):
        return sd.query_devices()

    def set_device(self, device):
        self._device = device
        self._sample_rate = sd.query_devices(self._device, 'input')['default_samplerate']

    def _callback_fn(self, indata, frames, time, status):
        if not any(indata):
            return

        if status:
            return

        data = indata.copy()

        if self._queue is not None:
            self._queue.put(data)

        if self._process_fn is not None:
            self._process_fn(data)

    def _main_loop(self):
        if not self._active:
            return

        with sd.InputStream(device=self._device,
                            channels=self._channel_cnt,
                            dtype="float32",   # "int16",
                            callback=self._callback_fn,
                            blocksize=self._samples_per_frame,
                            samplerate=self._sample_rate):
            while True:
                if not self._active:
                    break


class PAInputDevice(InputDevice):
    def __init__(self, device=None, channel_cnt=1, samples_per_frame=2048, queue_data=True, max_queue_len=200):
        super(PAInputDevice, self).__init__(device=device,
                                            channel_cnt=channel_cnt,
                                            samples_per_frame=samples_per_frame,
                                            queue_data=queue_data,
                                            max_queue_len=max_queue_len)

        self._stream = None

    @classmethod
    def available_devices(cls):
        output = ""
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                output += f"Input Device id {i} - {p.get_device_info_by_host_api_device_index(0, i).get('name')}\n"
        return output

    def start(self):
        self._stream = pyaudio.PyAudio().open(format=pyaudio.paFloat32,
                                              channels=self._channel_cnt,
                                              rate=self._sample_rate,
                                              input=True,
                                              input_device_index=self._device,
                                              frames_per_buffer=self._samples_per_frame)
        self._stream.start_stream()
        super(PAInputDevice, self).start()

    def stop(self):
        self._stream.start_stream()
        super(PAInputDevice, self).stop()

    def _callback_fn(self, indata, frames, time, status):
        if not any(indata):
            return

        if status:
            return

        if self._queue is not None:
            self._queue.put(indata)

        if self._process_fn is not None:
            self._process_fn(indata)

    def _main_loop(self):
        if not self._active:
            return

        while self._stream.is_active():
            self._callback_fn(self._stream.read(self._samples_per_frame), self._samples_per_frame, 0, 0)
            if not self._active:
                break
