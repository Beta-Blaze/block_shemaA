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


class Shape:
    def __init__(self, shape_id, master, x, y, text=""):
        if master not in SHAPE_TYPES:
            print("Illegal shape type")
            exit()
        self.id = shape_id
        self.master = SHAPE_TYPES[master]
        self.pos = [x, y]
        self.text = text

    def get_xml(self):
        return f"""<Shape ID='{self.id}' Type='Shape' Master='{self.master}'><Cell N='PinX' V='{self.pos[0]}'/>
        <Cell N='PinY' V='{self.pos[1]}'/>
        <Text>{self.text}</Text></Shape>
        """
