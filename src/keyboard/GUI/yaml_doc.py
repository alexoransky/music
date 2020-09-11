import yaml


class YamlDoc:
    def __init__(self, fpath):
        self.contents = {}
        self.error = self.load(fpath)

    def load(self, fpath):
        err = "Error reading the config file: {}".format(fpath)
        try:
            with open(fpath, 'rt', encoding='utf8') as cf:
                try:
                    self.contents = yaml.safe_load(cf)
                except yaml.YAMLError as exc:
                    print(err)
                    if hasattr(exc, 'problem_mark'):
                        mark = exc.problem_mark
                        descr = "YAML error at position L:{}, C:{}".format(mark.line + 1, mark.column + 1)
                        print(descr)
                        return err + "\n" + descr
        except:
            print(err)
            return err

        return None
