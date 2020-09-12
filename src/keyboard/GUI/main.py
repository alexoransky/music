import sys
import traceback

from PyQt5 import QtWidgets

from main_window import MainWindow
from utils import delete_file

from pprint import pprint
from termcolor import cprint

from audio import AudioSupport

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

    delete_file(EXCEPTION_LOG)
    sys.excepthook = exception_hook

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(app)
    main_window.show()

    sys.exit(app.exec_())
