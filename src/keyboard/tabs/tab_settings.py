from .tab import Tab


class Settings(Tab):
    def __init__(self, ui, tab, config, log_fn=print):
        super().__init__(ui, tab, config, enable_timer=False, log_fn=log_fn)

        self.width = 100
        self.height = 100

    def init_ui(self):
       pass

    def update_ui(self):
        pass

    def resize_widgets(self):
        # # stack tables one on top of another
        # self.table_tasks.move(4, 4)
        # self.table_network.move(4, ht + 12)
        # self.table_sys.move(4, ht + hn + 24)

        # calculate the size of the box around tables
        w = self.width
        h = self.height + 24
        return w, h

    def cleanup_ui(self):
        pass
