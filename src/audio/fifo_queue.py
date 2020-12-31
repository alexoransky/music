from queue import Queue
from multiprocessing import Queue as MPQueue
from collections import deque


# The class implements non-blocking FIFO queue.
# The queue can be either - regular queue or deque.
# It also can be limited in size.
class FIFOQueue:
    def __init__(self, multiprocess=False, is_deque=True, max_len=200):
        if multiprocess:
            is_deque = False

        self._queue = None
        self._use_deque = is_deque
        self._use_mpqueue = multiprocess
        if self._use_deque:
            if max_len == 0:
                max_len = None
            self._queue = deque(maxlen=max_len)
        else:
            if max_len is None:
                max_len = 0
            if self._use_mpqueue:
                self._queue = MPQueue(maxsize=max_len)
            else:
                self._queue = Queue(maxsize=max_len)

    def clear(self):
        if self._use_deque:
            self._queue.clear()
        else:
            while self._queue.get() is not None:
                pass

    def size(self):
        if self._use_deque:
            return len(self._queue)
        else:
            return self._queue.qsize()

    def put(self, x):
        if self._use_deque:
            self._queue.append(x)
        else:
            try:
                self._queue.put_nowait(x)
            except:
                return False
        return True

    def get(self):
        try:
            if self._use_deque:
                return self._queue.popleft()
            else:
                return self._queue.get_nowait()
        except:
            return None
