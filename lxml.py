from vsdx import Vsdx

v = Vsdx("1.vsdx")
v.open_vsdx_file()
input()
v.save_vsdx_file()


class Lxml:
    def __init__(self, filename):
        self.filename = filename
        self.shapes = []

    def generate_page_xml(self):
        temp = '''<?xml version='1.0' encoding='utf-8' ?>
<PageContents xmlns='http://schemas.microsoft.com/office/visio/2012/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships' xml:space='preserve'>
<Shapes>'''
        for i in self.shapes:
            temp += i.get_xml()
        temp += '''</Shapes>
</PageContents>'''
        return temp

    def write_file(self):
        with open(self.filename) as f:
            f.write(self.generate_page_xml())

    def add_shape(self, shape, direction, x, y):
        try:
            self.shapes[x][y]
        except Exception:
            print('всё плохо')
            exit()
        if direction == 'd':
            self.shapes.append([] * len(self.shapes[0]))

            self.shapes[x + 1][y] = shape
        if direction == 'r':
            self.shapes.append([] * len(self.shapes[0]))
            self.shapes = [i.append([]) for i in self.shapes]

            self.shapes[x + 1][y + 1] = shape
        if direction == 'l':
            self.shapes.append([] * len(self.shapes[0]))
            self.shapes = [[] + i for i in self.shapes]

            self.shapes[x + 1][y - 1] = shape
