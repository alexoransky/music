from dataclasses import dataclass
from yaml_doc import YamlDoc


@dataclass
class Loadable:
    _is_default: bool = True

    def load(self, data_dict):
        """
        Loads the object from the dictionary.  Updates each field but only when the field exists.
        Sets the _is_default flag to False if any of the values was updated.
        :param data_dict: the dictionary that defines values
        """
        if data_dict is None:
            return

        for key, value in data_dict.items():
            if hasattr(self, key):
                old_value = getattr(self, key, None)
                setattr(self, key, value)
                if (old_value is None) or (old_value != value):
                    self._is_default = False


class Config:
    @dataclass
    class MainWindow(Loadable):
        fixed_size: bool = False
        auto_shrink_to_screen: bool = True
        margin_x: int = 0
        margin_y: int = 0
        width: int = 1000
        height: int = 800
        min_width: int = 800
        min_height: int = 600

    @dataclass
    class KeyboardTab(Loadable):
        visible: bool = True
        timer: int = 1000
        start_note: str = "C"
        key_count: int = 88
        show_labels: bool = False

    @dataclass
    class SettingsTab(Loadable):
        visible: bool = True
        timer: int = 0

    def __init__(self, fpath: str):
        doc = YamlDoc(fpath)
        data = doc.contents
        self.error = doc.error

        self.main_window = self.MainWindow()
        self.main_window.load(data.get("main_window", None))

        self.tabs = {}
        self.tabs["keyboard_tab"] = self.KeyboardTab()
        self.tabs["settings_tab"] = self.SettingsTab()
        for name, tab in self.tabs.items():
            tab.load(data.get(name, None))


if __name__ == "__main__":
    config = Config("config.yml")
    print(config.main_window.height)
    print(config.main_window._is_default)
