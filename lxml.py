class Lxml:
    def __init__(self):
        self.filename = r"temp\visio\pages\page1.xml"
        self.shapes = [[[]]]

    def generate_page_xml(self):
        temp = '''<?xml version='1.0' encoding='utf-8' ?>
<PageContents xmlns='http://schemas.microsoft.com/office/visio/2012/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships' xml:space='preserve'>
<Shapes>'''
        for x in range(len(self.shapes)):
            for y in range(len(self.shapes[x])):
                if self.shapes[x][y]:
                    print(self.shapes[x][y])
                    self.shapes[x][y].set_position([x, y])
                    temp += self.shapes[x][y].get_xml()
        temp += '''</Shapes>
</PageContents>'''
        return temp

    def write_file(self):
        with open(self.filename, 'w') as f:
            f.write(self.generate_page_xml())

    def add_shape(self, shape, direction, x, y):
        try:
            self.shapes[x][y]
        except Exception:
            print('всё плохо')
            exit()
        if direction == 'd':
            self.shapes.append([[] * len(self.shapes[0][0])])
            print(self.shapes)
            self.shapes[x + 1][y] = shape
        if direction == 'r':
            self.shapes.append([[] * len(self.shapes[0][0])])
            self.shapes = [i + [[]] for i in self.shapes]

            self.shapes[x + 1][y + 1] = shape
        if direction == 'l':
            self.shapes.append([[] * len(self.shapes[0][0])])
            self.shapes = [[[]] + i for i in self.shapes]

            self.shapes[x + 1][y - 1] = shape
