import sys
import traceback

from PyQt5 import QtWidgets

from main_window import MainWindow
from utils import delete_file

EXCEPTION_LOG = "exception.log"


def exception_hook(type, value, trace):
    exc = "".join(traceback.format_exception(type, value, trace))
    with open(EXCEPTION_LOG, "w") as f:
        f.write(exc)

    print(exc)
    sys.exit(1)


if __name__ == "__main__":
    delete_file(EXCEPTION_LOG)
    sys.excepthook = exception_hook

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(app)
    main_window.show()

    sys.exit(app.exec_())
