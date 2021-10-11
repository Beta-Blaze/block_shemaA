SHAPE_TYPES = {
    "START": 2,
    "PROCESS": 4,
    "INPUT": 5,
    "IF": 6,
    "MODIFICATION": 9,
    "DEFINED_PROCESS": 12,
    "ONE_PAGE_CONNECTOR": 15,
    "MULTI_PAGE_CONNECTOR": 16
}

count = 1


class Shape:
    def __init__(self, master, text=""):
        global count
        if master not in SHAPE_TYPES:
            print("Illegal shape type")
            exit()
        self.id = count
        count += 1
        self.master = SHAPE_TYPES[master]
        self.text = text
        self.pos = []

    def set_position(self, pos):
        self.pos = pos

    def get_xml(self):
        return f"""<Shape ID='{self.id}' Type='Shape' Master='{self.master}'><Cell N='PinX' V='{self.pos[0]}'/>
        <Cell N='PinY' V='{self.pos[1]}'/>
        <Text>{self.text}</Text></Shape>
        """
