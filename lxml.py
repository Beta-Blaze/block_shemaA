import shape


class Lxml:
    def __init__(self):
        self.filename = r"temp\visio\pages\page1.xml"
        self.shapes = []
        self.cords = []

    def generate_page_xml(self):
        temp = '''<?xml version='1.0' encoding='utf-8' ?>
<PageContents xmlns='http://schemas.microsoft.com/office/visio/2012/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships' xml:space='preserve'>
<Shapes>'''
        for s in self.shapes:
            temp += s.get_xml()
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

    def add_shape(self, new_shape, direction, prev_shape=False):
        if not prev_shape:
            new_shape.set_position(0, 0)
            new_shape.type = 'base'
            self.shapes.append(new_shape)
            self.cords.append(new_shape.pos)
            return new_shape

        x, y = prev_shape.pos

        if direction == 'l':
            new_shape.set_position(x - 1, y - 1)

        elif direction == 'r':
            new_shape.set_position(x + 1, y - 1)

        elif direction == 'd':
            new_shape.set_position(x, y - 1)

        if new_shape.pos in self.cords:
            self.moves(new_shape, direction)

        new_shape.type = direction
        new_shape.from_s = prev_shape
        prev_shape.to_s = new_shape

        self.shapes.append(new_shape)
        self.cords.append(new_shape.pos)

        return new_shape
