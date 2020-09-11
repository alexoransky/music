import math
import json
import os
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView

TIME_NS_AVAIL = True
if not hasattr(time, "time_ns"):
    TIME_NS_AVAIL = False


def round(n, decimals=0, resolution=None):
    multiplier = 10 ** decimals
    if resolution is not None:
        multiplier *= (1.0 / resolution)

    result = math.floor(n * multiplier + 0.5) / multiplier

    if (decimals == 0) and (resolution is None):
        result = int(result)

    return result


def average(lst):
    cnt = len(lst)
    if cnt == 0:
        return 0.0

    total = 0
    for v in lst:
        total += v

    return total / cnt


def to_int(s):
    try:
        val = int(s)
    except:
        val = None
    return val


def percentage(numer, denom, decimals=3):
    if numer is None or denom is None or denom == 0:
        return None

    return round(numer * 100 / denom, decimals)


def set_table_scrollbars(table, hor_scrollbar, ver_scrollbar):
    if hor_scrollbar:
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    else:
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    if ver_scrollbar:
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    else:
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


def max_table_size(table, max_rows=None, max_cols=None):
    row_sb_needed = False
    col_sb_needed = False

    rows = table.rowCount()
    if max_rows is not None:
        if rows > max_rows:
            rows = max_rows
            row_sb_needed = True

    cols = table.columnCount()
    if max_cols is not None:
        if cols > max_cols:
            cols = max_cols
            col_sb_needed = True

    w = table.verticalHeader().width() + 2
    for i in range(cols):
        w += table.columnWidth(i)

    h = table.horizontalHeader().height() + 2
    for i in range(rows):
        h += table.rowHeight(i)

    return w, h, col_sb_needed, row_sb_needed


def beautify_table(table, max_rows=None, max_cols=None, dw=0, dh=0):
    w, h, sb_hor, sb_ver = max_table_size(table, max_rows=max_rows, max_cols=max_cols)
    w += dw
    h += dh

    table.setMaximumHeight(h)
    table.setMaximumWidth(w+2)
    table.resize(w, h)

    set_table_scrollbars(table, sb_hor, sb_ver)

    return w, h


def clear_table(table, start_row=0, stop_row=None, start_col=0, stop_col=None):
    # clear the table
    if stop_row == None:
        stop_row = table.rowCount()

    if stop_col == None:
        stop_col = table.columnCount()

    for row in range(start_row, stop_row):
        for col in range(start_col, stop_col):
            table.setItem(row, col, QTableWidgetItem(""))


def make_table_nonedit(table, nosel=True):
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setFocusPolicy(Qt.NoFocus)
    if nosel:
        table.setSelectionMode(QAbstractItemView.NoSelection)


def make_checkbox_nonedit(checkbox):
    checkbox.setAttribute(Qt.WA_TransparentForMouseEvents)
    checkbox.setFocusPolicy(Qt.NoFocus)


def make_checkbox_edit(checkbox):
    checkbox.setAttribute(Qt.WA_TransparentForMouseEvents, False)
    checkbox.setFocusPolicy(Qt.StrongFocus)


def make_edit_nonedit(edit):
    # edit.setAttribute(Qt.WA_TransparentForMouseEvents)
    edit.setFocusPolicy(Qt.NoFocus)


def validate_edit(edit, condition):
    if condition:
        edit.setStyleSheet("QLineEdit{color: green;}")
    else:
        edit.setStyleSheet("QLineEdit{color: red;}")


def write_to_json_file(fpath, data, mode="a", new_line=True):
    try:
        with open(fpath, mode) as f:
            s = json.dumps(data)
            if new_line:
                f.write(s + ",\n")
            else:
                s = s.replace("{", "\n{")
                f.write(s)
    except:
        return False

    return True


def read_from_json_file(fpath, MAX_CNT=None):
    if MAX_CNT is None:
        try:
            with open(fpath, 'r') as f:
                s = f.read()
        except:
            return None
    else:
        try:
            with open(fpath, 'r') as f:
                lst = f.readlines()
                if len(lst) > MAX_CNT:
                    lst = lst[-MAX_CNT:]
                s = "[" + "".join(lst)
                s = s[:-2] + "]"
        except:
            return None

    data = json.loads(s)
    return data


def delete_file(fpath):
    try:
        os.remove(fpath)
    except OSError as e:
        pass


def join_dir_fname(dir, fname, backslash=False):
    s = dir
    cnt = 0
    char = "/"
    if backslash:
        char = "\\"

    if dir[-1] == char:
        cnt += 1
    if fname[0] == char:
        cnt += 1

    if cnt == 0:
        s = s + char
    if cnt == 2:
        s = dir[:-1]

    s = s + fname
    return s


def mkdir(fpath):
    if not os.path.exists(fpath):
        try:
            os.makedirs(fpath)
        except:
            return False

    return True


def get_time_us():
    if TIME_NS_AVAIL:
        return int(time.time_ns() // 1000)

    return int(time.time() * 1000)


def bit(num, b):
    return (num & (1 << b)) >> b


def bit_set(num, b):
    return (num & (1 << b)) > 0


def screen_size(app):
    rec = app.desktop().screenGeometry()
    return rec.width(), rec.height()

def window_size(app):
    return app.width(), app.height()

def bswap_u16(x: int) -> int:
    lo = x & 0x00ff
    hi = x & 0xff00
    return ((lo << 8) & 0xff00) + ((hi >> 8) & 0x00ff)


def bswap_16(x: int) -> int:
    inv = bswap_u16(x)
    if inv > 6000:
        return inv - 65536
    return inv
