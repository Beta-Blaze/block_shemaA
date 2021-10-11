from vsdx import Vsdx

v = Vsdx("1.vsdx")
v.open_vsdx_file()
input()
v.save_vsdx_file()


class Lxml:
    def __init__(self, filename):
        self.filename = filename
        self.shapes = []

    def parse(self):
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
            f.write(self.parse())

    def add_shape(self, shape):
        self.shapes.append(shape)
