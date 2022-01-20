import sys
from parser import PathFilter, PyFilePaser

THIS_FILE = __file__.rstrip("co")


def set_tracer(tracer):
    print("Set tracer")
    sys.settrace(tracer)


def clear_tracer():
    sys.settrace(None)

class Tracer:
    def __init__(self, project_dir="./"):
        # only trarce files in this path
        self.project_path = ""
        # key filename  value FilePaser
        self.file_cache = {}
        self.path_manager = PathFilter(project_dir)
        self.state_manager = TraceState()
        # self.state_manager.count_total(self.path_manager.include_path)

    def is_include(self, path):
        return path.startswith(self.path_manager.project_path)

    def cache_file(self, filename):
        if filename not in self.file_cache.keys():
            self.file_cache[filename] = PyFilePaser(filename)

    def tranfer_line(self, filename, line_no):
        return self.file_cache[filename].map_line(line_no)

    def tracer_end(self):

        clear_tracer()
        self.state_manager.count_total(
            [file.filename for file in self.file_cache.values()]
        )
        self.state_manager.print_result()

    def tracer(self, frame, event, arg_unused):
        """core"""

        if THIS_FILE in frame.f_code.co_filename:
            return None

        filename = frame.f_code.co_filename
        lineo = frame.f_lineno
        func = frame.f_code.co_name + "()"

        if not self.is_include(filename):
            return self.tracer

        if not filename.startswith("<"):
            self.cache_file(filename)
        # print(frame.f_globals.get('__file__'))

        if event == "line":
            code = self.tranfer_line(filename, lineo)
            self.state_manager.add_line(code)
            print(func, code)
        return self.tracer


class TraceState:
    def __init__(self):
        self.line_coverage = 0.00
        self.traced_lines = []
        self.total_lines = 0

    def add_line(self, line):
        self.traced_lines.append(line)

    def count_total(self, files):
        """This method use to count the lines in this project"""

        if not len(files):
            raise Exception("There are no files inside include_list")

        self.total_lines = 0
        note_flag = False
        note_char = ""
        for file in files:
            lines = open(file).readlines()
            for line in lines:
                line = line.strip()
                if not len(line) or line == "\n":
                    continue
                if note_flag:
                    if line.endswith(note_char):
                        note_flag = False
                    continue
                if line.startswith("#"):
                    continue
                if line.startswith('"""' or "'''"):
                    note_char = line[:3]
                    if line.endswith(note_char):
                        continue
                    note_flag = True
                    continue
                self.total_lines += 1

    def print_result(self):
        lines = len(set(self.traced_lines))

        print("====" * 20)
        print(f"traced_lines { lines}")
        print(f"project lines {self.total_lines}")
        print(f"line_coverage:  { lines / self.total_lines:.2f}")
        print("====" * 20)
