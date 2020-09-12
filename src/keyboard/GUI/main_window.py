import sys
import traceback
from dataclasses import dataclass
from typing import Callable

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QTabWidget, QVBoxLayout, QStyle

from ui_main_window import Ui_MainWindow
from config import Config
from utils import screen_size, window_size
from tabs.tab_keyboard import Keyboard
from tabs.tab_settings import Settings

from audio import AudioSupport

TOOL_TITLE = "Digital Keyboard"
TOOL_VER = "1.0"
CONFIG_FILE = "config.yml"


@dataclass
class TabRef:
    widget: Callable
    make: Callable

# All tabs in the tool:
# Names must match the config.yml and ui_main_window.py files.
TABS = {
    # "status_tab": TabRef(lambda self: self.ui.status, lambda self, widget: Status(self.ui, widget, self.config)),
    # "connection_tab": TabRef(lambda self: self.ui.connection, lambda self, widget: Connection(self.ui, widget, self.config)),
    "keyboard_tab": TabRef(lambda self: self.ui.keyboard, lambda self, widget: Keyboard(self.ui, widget, self.config.tabs["keyboard_tab"])),
    "settings_tab": TabRef(lambda self: self.ui.settings, lambda self, widget: Settings(self.ui, widget, self.config.tabs["settings_tab"])),
}


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        app.setStyle("Breeze")
        app.aboutToQuit.connect(self.on_close)

        self.config = Config(CONFIG_FILE)

        # create GUI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # store tabs in a list so that we can iterate over them later
        # # create and show or hide optional tabs as per the config file
        self.tabs = []
        for tab_name, tab_config in self.config.tabs.items():
            if "_tab" in tab_name:
                ui_widget = TABS[tab_name].widget(self)
                if ui_widget is None:
                    continue
                if tab_config.visible:
                    tab = TABS[tab_name].make(self, ui_widget)
                    self.tabs.append(tab)
                else:
                    self.ui.tabs.removeTab(self.ui.tabs.indexOf(ui_widget))

        # sort the tab list in the order they appear on the main window
        self.tabs.sort(key=lambda t: self.ui.tabs.indexOf(t.tab_widget))

        # connect signals
        self.ui.tabs.currentChanged.connect(self.current_tab_changed)

        # initialize the main window and all tabs
        self.init_ui()

        # start MIDI
        self.audio = AudioSupport()
        if not self.audio.start_midi(self.config.main_window.port_in, self.config.main_window.port_out):
            self.log("Cannot start MIDI")

    def _set_size(self):
        cw = self.config.main_window.width
        ch = self.config.main_window.height

        if self.config.main_window.auto_shrink_to_screen:
            w, h = screen_size(self.app)
            # shrink to the screen dimensions and allow space for the task bar
            if cw > w:
                cw = w - 2*self.config.main_window.margin_x
            if ch > h:
                ch = h - 2*self.config.main_window.margin_y

        if self.config.main_window.fixed_size:
            self.setFixedWidth(cw)
            self.setFixedHeight(ch)
        else:
            self.setGeometry(0, 0, cw, ch)
            self.setGeometry(QStyle.alignedRect(QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
                                                self.size(), self.app.desktop().availableGeometry()))

        return cw, ch

    def init_ui(self):
        # set window title and size
        self.setWindowTitle(TOOL_TITLE)
        self.setMinimumSize(self.config.main_window.min_width, self.config.main_window.min_height)
        w, h = self._set_size()

        # status bar
        self.ui.statusbar.showMessage("Initializing...")

        # tabs
        for tab in self.tabs:
            tab.init_ui()

            # resize the tab
            tab.tab_widget.setGeometry(0, 0, w-24, h-64)

        for tab in self.tabs:
            tab.resize_ui()

        # log the tool name and ver
        self.log(f"{TOOL_TITLE} v{TOOL_VER}")

        # display possible config error
        self.log(self.config.error)

        # display the first tab
        self.ui.tabs.setCurrentIndex(0)
        self.current_tab_changed(0)

    def log(self, s):
        if s is None:
            return
        print(s)

    def current_tab_changed(self, index):
        print("Tab changed")
        for tab in self.tabs:
            if tab.ui_timer is not None:
                tab.ui_timer.stop()

        if self.tabs[index].ui_timer is not None:
            self.tabs[index].ui_timer.start()

        self.tabs[index].resize_ui()

    def resizeEvent(self, event):
        print("Resize event")
        QMainWindow.resizeEvent(self, event)

        for tab in self.tabs:
            tab.resize_ui()

    def on_close(self):
        print("Closing the main window")
        self.audio.stop_midi()
        for tab in self.tabs:
            tab.on_close()
