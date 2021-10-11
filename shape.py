class Shape:
    def __init__(self, shape_id, master, x, y, text=""):
        self.id = shape_id
        self.master = master
        self.pos = [x, y]
        self.text = text

    def get_xml(self):
        return f"""<Shape ID='{self.id}' Type='Shape' Master='{self.master}'><Cell N='PinX' V='{self.pos[0]}'/>
        <Cell N='PinY' V='{self.pos[1]}'/>
        <Text>{self.text}</Text></Shape>
        """
