from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtGui import QTextCursor


class Tab:
    def __init__(self, ui, ui_tab_widget, config, enable_timer=True, log_fn=None):
        self.ui = ui
        self.tab_widget = ui_tab_widget
        self.config = config
        self.log_fn = log_fn

        if enable_timer:
            self.ui_timer = QTimer()
            self.ui_timer.timeout.connect(self.update_ui)
        else:
            self.ui_timer = None

    def init_ui(self):
        """
        This function will be called from the main window.
        :return: none
        """
        pass

    def update_ui(self):
        """
        This method is called periodically to update GUI if the tab's timer is enabled.
        :return: none
        """
        pass

    def resize_widgets(self):
        """
        Override this method to
        1. resize all tab widgets when needed(e.g. a row was added to the table)
        2. move widgets to their new positions
        3. calculate the size of the containment box for the widgets of the tab
        :return: width and height of the containment box
        """
        width = 0
        height = 0
        return width, height

    def resize_ui(self):
        """
        This method will be triggered by the Resize event.
        The main goal is to provide scrolling for the tab.
        Override this function only when absolutely necessary.
        Normally, resize_widgets() should be used instead.
        It is assumed that each tab has a scroll area that is called scrollArea_<tab name>.
        :return: none
        """
        w = self.tab_widget.size().width()
        h = self.tab_widget.size().height()
        sa_name = "scrollArea_" + self.tab_widget.objectName()
        sa = getattr(self.ui, sa_name)
        sa.setGeometry(0, 0, w, h)

        w, h = self.resize_widgets()
        if w != 0:
            sa.widget().setGeometry(QRect(0, 0, w+4, h+4))

    def stop_ui_updates(self):
        """
        This function will be called from the main window.
        :return: none
        """
        if self.ui_timer is not None:
            self.ui_timer.stop()

    def start_ui_updates(self):
        """
        This function will be called from the main window.
        :return: none
        """
        if self.ui_timer is not None:
            self.ui_timer.start(self.config["timer"])

    def log(self, text):
        if self.log_fn is None:
            return

        self.log_fn(text)

    def on_close(self):
        if self.ui_timer is not None:
            self.ui_timer.stop()
