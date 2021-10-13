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

id_shape_counter = 1


class Shape:
    def __init__(self, master, text=""):
        global id_shape_counter
        if master not in SHAPE_TYPES:
            print("Illegal shape type")
            exit()
        self.id = id_shape_counter
        id_shape_counter += 1
        self.master = SHAPE_TYPES[master]
        self.text = text
        self.pos = []
        self.size = SHAPE_SIZE[master]

    def set_position(self, pos):
        self.pos = pos

    def get_xml(self):
        return f"""<Shape ID='{self.id}' Type='Shape' Master='{self.master}'><Cell N='PinX' V='{self.pos[0]}'/>
        <Cell N='PinY' V='{self.pos[1]}'/>
        <Text>{self.text}</Text></Shape>
        """
