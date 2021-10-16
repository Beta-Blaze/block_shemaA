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

    def add_shape(self, new_shape, direction, prew_shape=False):
        if not prew_shape:
            new_shape.set_position(0, 0)
            self.shapes.append(new_shape)
            self.cords.append(new_shape.pos)
            return new_shape

        if direction == 'l':
            x, y = prew_shape.pos
            new_shape.set_position(x - 1, y - 1)
            while new_shape.pos in self.cords:
                x, y = new_shape.pos
                new_shape.set_position(x - 1, y)

        elif direction == 'r':
            x, y = prew_shape.pos
            new_shape.set_position(x + 1, y - 1)
            while new_shape.pos in self.cords:
                x, y = new_shape.pos
                new_shape.set_position(x + 1, y)

        elif direction == 'd':
            x, y = prew_shape.pos

            new_shape.set_position(x, y - 1)

            new_shape.from_s = prew_shape
            prew_shape.to_s = new_shape

            while new_shape.pos in self.cords:
                x, y = new_shape.pos
                new_shape.set_position(x, y + 1)

            self.shapes.append(new_shape)
            self.cords.append(new_shape.pos)

        return new_shape
