from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QGraphicsRectItem, QGraphicsTextItem, QGraphicsScene, QGraphicsView
from tab import Tab
# from kbd_widgets import KeyboardWidget

KEYS = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
WHITE_KEYS = ["A", "B", "C", "D", "E", "F", "G"]
# sizes in inches
WHITE_KEY_LENGTH = 6
WHITE_KEY_WIDTH = 7/8
BLACK_KEY_LENGTH = 3 + 15/16
BLACK_KEY_WIDTH = 15/32
WHITE_KEY_GAP = 1/32
# normalized key sizes
NORM_WHITE_KEY_LENGTH = round(WHITE_KEY_LENGTH / WHITE_KEY_GAP)
NORM_WHITE_KEY_WIDTH = round(WHITE_KEY_WIDTH / WHITE_KEY_GAP)
NORM_BLACK_KEY_LENGTH = round(BLACK_KEY_LENGTH / WHITE_KEY_GAP)
NORM_BLACK_KEY_WIDTH = round(BLACK_KEY_WIDTH / WHITE_KEY_GAP)
NORM_WHITE_KEY_GAP = 1
BW_RATIO = NORM_BLACK_KEY_WIDTH / NORM_WHITE_KEY_WIDTH


class Keyboard(Tab):
    def __init__(self, ui, tab, config, log_fn=print):
        super().__init__(ui, tab, config, enable_timer=False, log_fn=log_fn)

        self.ui = ui
        self.tab = tab
        self.config = config

        self.keyboard_widget = KeyboardWidget(config.key_count, config.start_note, config.show_labels, parent=ui.widget_keyboard)

    def init_ui(self):
        self.resize_widgets()

    def update_ui(self):
        pass

    def resize_widgets(self):
        w = self.ui.scrollArea_keyboard.width()
        h = self.ui.scrollArea_keyboard.height()

        w -= 8
        h -= 8
        self.ui.groupBox_keyboard.resize(w, h)
        self.ui.groupBox_keyboard.move(4, 4)

        self.keyboard_widget.init_ui(w, h)

        return w, h

    def cleanup_ui(self):
        self.log("keyboard tab: cleanup_ui")


class KeyboardWidget(QGraphicsView):
    def __init__(self, key_count: int, start_note: str, show_labels: bool, parent):
        super().__init__(parent)

        self.widget = parent
        self.key_area = None
        self.keys = []
        self.key_cnt = key_count
        self.start_note = start_note
        self.show_labels = show_labels

        self.white_key_width = 0
        self.black_key_width = 0
        self.white_key_gap = 0
        self.white_key_height = 0
        self.black_key_height = 0

    def init_ui(self, max_w, max_h):
        self.widget.move(0, max_h * 0.5)
        self.widget.resize(max_w, max_h * 0.5)

        w = self.widget.width()
        h = self.widget.height()
        dw, dh = self._desired_size(w, h)

        self.widget.move(0, max_h-dh)
        self.widget.resize(dw, dh)
        self.move(0, 0)
        self.resize(dw, dh)
        self.show()

        self.key_area = QRect(0, 0, dw, dh)
        self.draw_keys()

        scene = QGraphicsScene(self)
        for key in self.keys:
            scene.addItem(key)
            if self.show_labels and key.label is not None:
                scene.addItem(key.label)
        self.setScene(scene)

        self.update_ui()

    def update_ui(self):
        self.scene().update(self.scene().sceneRect())

    def resize_widgets(self):
        w = self.ui.scrollArea_keyuboard.width()
        h = self.ui.scrollArea_keyboard.height()

        self.widget.move(0, h * 0.6)
        self.widget.resize(w, h * 0.4)

        return w, h

    def _idx_to_note(self, idx):
        start_idx = 0
        for k, i in enumerate(KEYS):
            if k == self.start_note:
                start_idx = i

        i = (start_idx + idx) % len(KEYS)
        return KEYS[i]

    def _white_key_cnt(self):
        white_key_cnt = 0
        for i in range(self.key_cnt):
            note = self._idx_to_note(i)
            if note in WHITE_KEYS:
                white_key_cnt += 1
        return white_key_cnt

    def _desired_size(self, max_width, max_height):
        # normalize the key width and length, assume gap is 1
        # total width is cnt of white keys + (cnt-1) gaps
        cnt = self._white_key_cnt()
        norm_width = NORM_WHITE_KEY_WIDTH * cnt + (cnt - 1)
        norm_height = NORM_WHITE_KEY_LENGTH

        r = norm_height / norm_width
        rw = max_width / norm_width

        w = int(max_width)
        h = int((max_width) * r)
        if h > max_height:
            h = int(max_height)

        while True:
            if int(rw) < 1:
                break
            w = int(norm_width * rw)
            h = int(norm_width * rw * r)
            if h <= max_height and w <= max_width:
                break
            rw -= 1

        fw = w / norm_width
        fh = h / norm_height
        self.white_key_width = int(NORM_WHITE_KEY_WIDTH * fw)
        self.black_key_width = int(NORM_BLACK_KEY_WIDTH * fw)
        self.white_key_gap = int(NORM_WHITE_KEY_GAP * fw)
        self.white_key_height = int(NORM_WHITE_KEY_LENGTH * fh) - 5
        self.black_key_height = int(NORM_BLACK_KEY_LENGTH * fh) - 5

        return w, h

    def draw_keys(self):
        self.keys.clear()

        # create white keys
        i = 0
        for idx in range(self.key_cnt):
            note = self._idx_to_note(idx)
            if note in WHITE_KEYS:
                x = self.key_area.x() + i * self.white_key_width
                if i > 0:
                    x += i * self.white_key_gap
                y = self.key_area.y()
                i += 1
                rect = QRect(x, y, self.white_key_width, self.white_key_height)
                key = KeyWidget(rect, idx, note)
                self.keys.append(key)

        # create black keys
        i = 0
        last_note = self.start_note
        last_x = 0
        for idx in range(self.key_cnt):
            note = self._idx_to_note(idx)
            if note in WHITE_KEYS:
                x = self.key_area.x() + i * self.white_key_width
                if i > 0:
                    x += i * self.white_key_gap
                last_note = note
                last_x = x
                i += 1
            else:
                if last_note in ["C", "F"]:
                    x = last_x + self.white_key_width - self.black_key_width * 0.65
                elif last_note in ["D", "A"]:
                    x = last_x + self.white_key_width - self.black_key_width * 0.35
                elif last_note == "G":
                    x = last_x + self.white_key_width - self.black_key_width * 0.5
                else:
                    continue
                y = self.key_area.y()
                rect = QRect(x, y, self.black_key_width, self.black_key_height)
                key = KeyWidget(rect, idx, note)
                self.keys.append(key)


class KeyWidget(QGraphicsRectItem):
    def __init__(self, rect: QRect, idx: int, note: str):
        super().__init__(rect.x(), rect.y(), rect.width(), rect.height())

        self.rect = rect
        self.idx = idx
        self.note = note
        self.label = None

        self.setBrush(Qt.black)

        if note in WHITE_KEYS:
            self.setBrush(Qt.white)
            # set the label
            self.label = QGraphicsTextItem()
            self.label.setDefaultTextColor(Qt.black)
            # font = self.label.font()
            # font.setBold(True)
            # self.label.setFont(font)
            self.label.setZValue(100)
            self.label.setPlainText(note)
            self.label.setPos(self.rect.x() + self.rect.width() / 2 - self.label.boundingRect().width() / 2,
                              self.rect.y() + self.rect.height() * 0.8)
