from queue import Queue
import mido


# This module is inspired by:
# https://github.com/icaroferre/MIDIRouter


MAX_MESSAGE_QUEUE_SIZE = 100


class MIDIPort:
    def __init__(self, name: str = None, port=None, message_filter=None):
        self.name = name
        self.port = port
        self.filter = None
        self.set_filter(message_filter)

    def open(self, port_name, output=True, callback=None):
        self.close()

        if output:
            try:
                self.port = mido.open_output(port_name, autoreset=True)
                self.port.reset()
            except:
                self.port = None
                return
        else:
            try:
                self.port = mido.open_input(port_name, callback=callback)
            except:
                self.port = None
                return

        self.name = port_name

    def close(self):
        self.name = None

        if self.port is None:
            return

        try:
            self.port.close()
        except:
            pass

        self.port = None

    def send(self, message):
        if self.port is None:
            return

        if self.filter is not None:
            if message.type in self.filter:
                return

        try:
            self.port.send(message)
        except:
            pass

    def set_filter(self, message_filter=None):
        """
        Deines the filter for send()
        :param message_filter: a list of Mido Message types, ex "aftertouch"
        :return:
        """
        if message_filter is None:
            self.filter = None
            return

        self.filter = []
        for msg in message_filter:
            self.filter.append(msg)

    def is_open(self):
        return self.port is not None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class MIDIRouter:
    def __init__(self, port_in: str = None, port_out: str = None, message_filter=None):
        self.port_in = MIDIPort()
        self.port_out = MIDIPort(message_filter=message_filter)

        self.enabled = False
        self.messages = Queue(maxsize=MAX_MESSAGE_QUEUE_SIZE)

        if port_in is not None:
            self.port_in.open(port_in, output=False, callback=self.input_message_handler)

        if port_out is not None:
            self.port_out.open(port_out, output=True)

    @classmethod
    def available_ports(cls, output=True):
        if output:
            return mido.get_output_names()

        return mido.get_input_names()

    def open_port(self, port: str, output=False):
        if port is None or port == "":
            return

        if output:
            self.port_out.open(port, output=True)
        else:
            self.port_in.open(port, output=False, callback=self.input_message_handler)

    def input_message_handler(self, message):
        if not self.enabled:
            return

        self.port_out.send(message)

        try:
            self.messages.put_nowait(message)
        except:
            pass

    def get_message(self):
        try:
            message = self.messages.get_nowait()
        except:
            return None

        return message

    def put_message(self, message):
        self.port_out.send(message)

        try:
            self.messages.put_nowait(message)
        except:
            pass

    def clear_messages(self):
        while True:
            if self.get_message() is None:
                return

    def start(self):
        self.enabled = self.port_in.is_open() and self.port_out.is_open()
        return self.enabled

    def stop(self):
        self.enabled = False
        self.port_in.close()
        self.port_out.close()
        self.clear_messages()
