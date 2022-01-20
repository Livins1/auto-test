import os
import re


class PyFilePaser:
    def __init__(self, filename):
        self.filename = filename
        self.text = ""
        self.source = ""

        self.__load_file()
        self.__load_lines()

    def __load_file(self):
        """load source code"""
        with open(self.filename, "r") as f:
            source = f.read()
            if source and source[-1] != "\n":
                source += "\n"
            self.source = source

    def __load_lines(self):
        """load to lines"""
        if self.source:
            self.lines = self.source.splitlines()
        else:
            raise Exception("Source is not loaded.")

    def map_line(self, line_no):
        return self.lines[line_no - 1]


class PathFilter:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.include_path = []
        # files only inside this path can be trace
        self.project_path = ""
        # support ./ or abs path
        self.__set_abs_path()
        self.__cache_paths()

    def __set_abs_path(self):
        if os.path.isabs(self.project_dir):
            self.project_path = self.project_dir
            return

        if self.project_dir == "./":
            self.project_path = os.path.dirname(os.path.abspath(__file__))
            return

        raise NotImplementedError

    def __cache_paths(self):
        for i, (dirpath, dirnames, filenames) in enumerate(os.walk(self.project_dir)):
            if i > 0 and "__init__.py" not in filenames:
                del dirnames[:]
                continue
            for filename in filenames:
                if re.match(r"^[^.#~!$@%^&*()+=,]+\.pyw?$", filename):
                    self.include_path.append(os.path.join(dirpath, filename))


if __name__ == "__main__":
    r = PyFilePaser("./main.py")
    r._load_file()
    r._load_lines()
