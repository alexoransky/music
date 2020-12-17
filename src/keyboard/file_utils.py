import os


def delete(fpath):
    try:
        os.remove(fpath)
    except OSError as e:
        pass
