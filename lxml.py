from vsdx import Vsdx

v = Vsdx("1.vsdx")
v.open_vsdx_file()
input()
v.save_vsdx_file()


class Shape():
    def __init__(self, shape_id, master, x, y, text=""):
        self.id = shape_id
        self.master = master
        self.pos = [x, y]
        self.text = text

    def get_xml(self):
        return f"""
        """


class Lxml:
    def __init__(self, filename):
        self.filename = filename

    def open_file(self):
        with open(self.filename) as f:
            self.content = ''.join(f.readlines()[1:])

    def parse(self):
        ...
