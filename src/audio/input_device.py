from threading import Thread
from multiprocessing import Process
from audio.fifo_queue import FIFOQueue

import sounddevice as sd
import pyaudio


class InputDevice:
    DEFAULT_SAMPLE_RATE = 48000

    def __init__(self, device, channel_cnt: int, samples_per_frame: int,
                 queue_data: bool, max_queue_len: int,
                 multiprocess: bool):
        self._device = device
        self._sample_rate = InputDevice.DEFAULT_SAMPLE_RATE
        self._channel_cnt = channel_cnt

        self._multiprocess = multiprocess
        self._active = False
        self._thread = None

        self._samples_per_frame = samples_per_frame

        # data will either be queued or processed by the supplied process function
        self._process_fn = None
        self._queue = None
        self._queue_data = queue_data
        if self._queue_data:
            self._queue = FIFOQueue(multiprocess=multiprocess, max_len=max_queue_len)

        # stats
        self.sample_cnt = 0
        self.sample_error_cnt = 0
        self.queue_error_cnt = 0

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
        """
        Use this method to set the process function for the received data when the data is NOT queued.
        :param process_fn: user-supllied function to process data
        """
        if self._queue_data:
            self._process_fn = None
            return

        self._process_fn = process_fn

    def data_is_queued(self):
        return self._queue_data

    def start(self):
        """
        This methods starts data reception.
        Overwrite this method to add functionality to actully start the device.
        :return:
        """
        self._active = True
        if self._multiprocess:
            self._thread = Process(target=self._main_loop)
        else:
            self._thread = Thread(target=self._main_loop)
        self._thread.start()

    def stop(self):
        """
        This method stops data reception.
        Overwrite this method to actually stop the device.
        :return:
        """
        self._active = False
        self._thread.join()

    def get_data(self):
        """
        This method returnes the data from the queue (when the data is queued)
        :return:
        """
        if self._queue is None:
            return None
        return self._queue.get()

    def queue_size(self):
        if self._queue is None:
            return None
        return self._queue.size()

    def _data_copy(self, data):
        """
        This method is used when the data that is read from a device, such as SoundDevice,
         needs to be buffered before it can be processed.
         SoundDevice data needs data[:, 0  or data.copy to be copied.
         Overwrite this method if other way to buffer data is needed.
        :param data: raw data from the device's stream
        :return: a copy of the supplied data
        """
        return data.copy()   # data[:, 0]

    def _callback_fn(self, indata, frames, time, status):
        """
        This method is used as a callback in SoundDevice and other streams.
        Most likely, there is no need to overwrite it.
        """
        if not any(indata):
            return

        if status:
            self.sample_error_cnt += 1
            return

        self.sample_cnt += 1

        if self._queue_data:
            if self._queue is not None:
                if not self._queue.put(self._data_copy(indata)):
                    self.queue_error_cnt += 1
            return

        if self._process_fn is not None:
            self._process_fn(self._data_copy(indata))

    def _main_loop(self):
        """
        Overwrite this method to receive the data from the device
        """
        if not self._active:
            return


class SDInputDevice(InputDevice):
    def __init__(self, device=None, channel_cnt=1, samples_per_frame=2048,
                 queue_data=True, max_queue_len=5,
                 multiprocess=True):

        super(SDInputDevice, self).__init__(device=device,
                                            channel_cnt=channel_cnt,
                                            samples_per_frame=samples_per_frame,
                                            queue_data=queue_data,
                                            max_queue_len=max_queue_len,
                                            multiprocess=multiprocess)

        if device is not None:
            self.set_device(device)

    @classmethod
    def available_devices(cls):
        return sd.query_devices()

    @classmethod
    def default_device(cls):
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            try:
                max_ch = sd.query_devices(i, 'input')['max_input_channels']
            except:
                continue
            if max_ch > 0:
                return i
        return None

    @classmethod
    def device_name(cls, dev_no):
        try:
            name = sd.query_devices(dev_no)["name"]
        except:
            return None
        return name

    def set_device(self, device):
        self._device = device
        self._sample_rate = sd.query_devices(self._device, 'input')['default_samplerate']

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
    def __init__(self, device=None, channel_cnt=1, samples_per_frame=2048,
                 queue_data=True, max_queue_len=5,
                 multiprocess=True):

        super(PAInputDevice, self).__init__(device=device,
                                            channel_cnt=channel_cnt,
                                            samples_per_frame=samples_per_frame,
                                            queue_data=queue_data,
                                            max_queue_len=max_queue_len,
                                            multiprocess=multiprocess)

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

    def _data_copy(self, data):
        return data

    def _main_loop(self):
        if not self._active:
            return

        while self._stream.is_active():
            self._callback_fn(self._stream.read(self._samples_per_frame), self._samples_per_frame, 0, 0)
            if not self._active:
                break
