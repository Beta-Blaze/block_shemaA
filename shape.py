SHAPE_TYPES = {
    "START": 2,
    "PROCESS": 4,
    "INPUT": 5,
    "IF": 6,
    "MODIFICATION": 7,
    "DEFINED_PROCESS": 8,
    "ONE_PAGE_CONNECTOR": 9,
    "MULTI_PAGE_CONNECTOR": 10
}

SHAPE_SIZE = {
    # Height Width
    "START": [0.3937007874015748, 1.181102362204724],
    "PROCESS": [0.7874015748031495, 1.181102362204724],
    "INPUT": [0.7874015748031495, 1.181102362204724],
    "IF": [0.7874015748031495, 1.181102362204724],
    "MODIFICATION": [0.7874015748031491, 1.181102362204724],
    "DEFINED_PROCESS": [0.7874015748031495, 1.181102362204724],
    "ONE_PAGE_CONNECTOR": [0.3937007874015748, 0.3937007874015748],
    "MULTI_PAGE_CONNECTOR": [0.4724409448818898, 0.3937007874015749]
}


class Shape:
    def __init__(self, shape_id, master, text="", shape_type=None, cords=None, shapes=None, from_s=None):
        if master not in SHAPE_TYPES:
            print("Illegal shape type")
            exit()
        self.shape_id = shape_id
        self.master = SHAPE_TYPES[master]
        self.text = text
        self.pos = []
        self.size = SHAPE_SIZE[master]
        self.to_s = []
        self.from_s = from_s
        self.shape_type = shape_type
        self.cords = cords
        self.shapes = shapes

    def set_position(self, x, y):
        self.pos = [x, y]

    def move(self, vector, direction=''):
        if self.shape_type == "base":
            return

        if vector == 'r':
            self.pos[0] += 1.5

        if vector == 'l':
            self.pos[0] -= 1.5

        for i in self.shapes:
            i: Shape
            if self.pos == i.pos and self != i:
                i.move(vector)

        if not direction or direction == 'd':
            for i in self.to_s:
                i.move(vector, 'd')
        if not direction or direction == 'a':
            self.from_s.move(vector, 'a')

    def get_xml(self):
        return f"""<Shape ID='{self.shape_id}' Type='Shape' Master='{self.master}'><Cell N='PinX' V='{self.pos[0]}'/>
        <Cell N='PinY' V='{self.pos[1]}'/>
        <Text>{self.text}</Text></Shape>
        """
