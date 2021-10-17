import shape
from connector import Connector

class Lxml:
    def __init__(self):
        self.filename = r"temp\visio\pages\page1.xml"
        self.shapes = []
        self.connectors = []
        self.cords = []
        self.first_if = True

    def generate_page_xml(self):
        temp = '''<?xml version='1.0' encoding='utf-8' ?>
<PageContents xmlns='http://schemas.microsoft.com/office/visio/2012/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships' xml:space='preserve'>
<Shapes>'''
        for s in self.shapes:
            temp += s.get_xml()
        for i in self.connectors:
            temp += i.get_xml()
        temp += '''</Shapes>
</PageContents>'''
        return temp

    def write_file(self):
        with open(self.filename, 'w', encoding="utf-8") as f:
            f.write(self.generate_page_xml())

    def moves(self, new_shape, direction):
        for i in self.shapes:
            i: shape.Shape
            if new_shape.pos == i.pos:
                i.move(direction)

    def add_connector(self, from_shape, to_shape, connector_position):
        c = Connector(from_shape, to_shape, connector_position)
        self.connectors.append(c)

    def add_shape(self, master, text, direction, prev_shape=None):
        if not prev_shape:
            new_shape = shape.Shape(master, text, 'base', self.cords, self.shapes)
            new_shape.set_position(5, 5)
            self.shapes.append(new_shape)
            self.cords.append(new_shape.pos)

            if new_shape.master == shape.SHAPE_TYPES["IF"] and self.first_if:
                self.first_if = False

            return new_shape

        x, y = prev_shape.pos

        new_shape = shape.Shape(master, text, direction, self.cords, self.shapes, prev_shape)

        if direction == 'l':
            new_shape.set_position(x - 1.5, y - 1)

        elif direction == 'r':
            new_shape.set_position(x + 1.5, y - 1)

        elif direction == 'd':
            new_shape.set_position(x, y - 1)

        if new_shape.pos in self.cords:
            self.moves(new_shape, direction)

        prev_shape.to_s.append(new_shape)

        self.shapes.append(new_shape)
        self.cords.append(new_shape.pos)

        if master == shape.SHAPE_TYPES["IF"] and self.first_if:
            new_shape.shape_type = "base"
            self.first_if = False

        return new_shape
