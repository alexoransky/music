from copy import copy
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem, QGraphicsScene, QGraphicsView
from audio.audio import AudioSupport
from theory.chords import Chord
from theory.notes import Note
from .tab import Tab


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
        super().__init__(ui, tab, config, enable_timer=True, log_fn=log_fn)

        self.ui = ui
        self.tab = tab
        self.config = config
        self.log = log_fn
        self.notes = set()

        self.keyboard_widget = KeyboardWidget(config.key_count, config.start_note, config.show_labels, parent=ui.widget_keyboard)

        # start MIDI
        self.audio = AudioSupport()
        self.audio_started = self.audio.start_midi(config.port_in, config.port_out)
        if self.audio_started:
            self.audio.parser.set_note_on_off_fn(self.note_fn)
        else:
            self.log("Cannot start MIDI")

    def init_ui(self):
        self.resize_widgets()

    def update_ui(self):
        notes, chord = self.audio.parser.get_notes(self.notes)
        notes_str = ""
        chord_str = ""
        if len(notes):
            notes_str = " ".join([note.name(octave=True) for note in notes])
            if chord is not None:
                ch = Chord(notes[0].name() + chord, notes[0].octave)
                notes_str += "  =  " + str(ch.name())
        self.ui.label_notes.setText(notes_str)

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

    def note_fn(self, note, is_on):
        self.notes = copy(self.audio.parser.notes)
        self.keyboard_widget.update_key(note, is_on)

    def on_close(self):
        self.audio.stop_midi()
        super().on_close()


class KeyboardWidget(QGraphicsView):
    def __init__(self, key_count: int, start_note: str, show_labels: bool, parent):
        super().__init__(parent)

        self.widget = parent
        self.key_area = None

        self.keys = []
        self.key_cnt = key_count
        self.start_note = start_note
        idx = Note.note_name_to_midi_number(start_note)
        self.midi_range = (idx, idx+key_count-1)

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

        # sort the keys by the key index
        self.keys.sort(key=lambda k: k.idx)

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
        for i, k in enumerate(KEYS):
            if k == self.start_note[0]:  # skip the octave
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
        last_note = self.start_note[0]  # skip the octave
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

    def _midi_note_to_idx(self, midi_note):
        return midi_note - self.midi_range[0]

    def update_key(self, midi_note, is_pressed):
        out_of_range = False
        idx = self._midi_note_to_idx(midi_note)
        # TODO: in case of chords outside of the piano range, need to shift up or down the entire chord (pressed keys)
        while idx < 0:
            idx += 12
            out_of_range = True
        while idx > self.key_cnt-1:
            idx -= 12
            out_of_range = True

        if is_pressed:
            self.keys[idx].press(out_of_range)
        else:
            self.keys[idx].release()

        self.update_ui()


class KeyWidget(QGraphicsRectItem):
    def __init__(self, rect: QRect, idx: int, note: str):
        super().__init__(rect.x(), rect.y(), rect.width(), rect.height())

        self.rect = rect
        self.idx = idx
        self.note = note
        self.label = None

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
        else:
            self.setBrush(Qt.black)

    def press(self, out_of_range=False):
        if out_of_range:
            self.setBrush(Qt.yellow)
        else:
            self.setBrush(Qt.gray)

    def release(self):
        if self.note in WHITE_KEYS:
            self.setBrush(Qt.white)
        else:
            self.setBrush(Qt.black)
