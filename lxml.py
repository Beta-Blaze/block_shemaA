class Lxml:
    def __init__(self):
        self.filename = r"temp\visio\pages\page1.xml"
        self.shapes = [[0]]

    def generate_page_xml(self):
        temp = '''<?xml version='1.0' encoding='utf-8' ?>
<PageContents xmlns='http://schemas.microsoft.com/office/visio/2012/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships' xml:space='preserve'>
<Shapes>'''
        for x in range(len(self.shapes)):
            for y in range(len(self.shapes[x])):
                if self.shapes[x][y]:
                    self.shapes[x][y].set_position([y, -x])
                    temp += self.shapes[x][y].get_xml()
        temp += '''</Shapes>
</PageContents>'''
        return temp

    def write_file(self):
        with open(self.filename, 'w', encoding="utf-8") as f:
            f.write(self.generate_page_xml())

    def add_shape(self, shape, direction, x, y):
        self.shapes.append([0 for _ in range(len(self.shapes[0]))])

        if direction == 'd':
            self.shapes[x + 1][y] = shape

        if direction == 'r':
            try:
                self.shapes[x + 1][y + 1]
            except Exception:
                self.shapes = [i + [0] for i in self.shapes]
            self.shapes[x + 1][y + 1] = shape

        if direction == 'l':
            if y < 1:
                y = 0
                self.shapes = [[0] + i for i in self.shapes]
                self.shapes[x + 1][y] = shape
            else:
                self.shapes[x + 1][y - 1] = shape

