import sys
import traceback
from pprint import pprint
from termcolor import cprint

from PyQt5 import QtWidgets

from audio.audio import AudioSupport

from keyboard.main_window import MainWindow
from keyboard.file_utils import delete


TOOL_TITLE = "Digital Keyboard"
TOOL_VER = "1.0"
CONFIG_FILE = "keyboard_config.yml"
EXCEPTION_LOG = "exception.log"


def exception_hook(type, value, trace):
    exc = "".join(traceback.format_exception(type, value, trace))
    with open(EXCEPTION_LOG, "w") as f:
        f.write(exc)

    print(exc)
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "-l":
            in_ports, out_ports = AudioSupport.available_midi_ports()

            cprint("Input MIDI ports:", "blue")
            pprint(in_ports)
            cprint("Output MIDI ports:", "blue")
            pprint(out_ports)

            sys.exit(0)

    delete(EXCEPTION_LOG)
    sys.excepthook = exception_hook

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(app, CONFIG_FILE, TOOL_TITLE, TOOL_VER)
    main_window.show()

    sys.exit(app.exec_())
