from visio import SHAPE_SIZE, SHAPE_TYPES


class Shape:
    def __init__(self, shape_id, master: str, text='', shape_type='', cords: [[]] = None, shapes: [] = None, from_s=None, flag_end=False):
        if master not in SHAPE_TYPES:
            print("Illegal shape type")
            exit()
        self.shape_id = shape_id
        self.master = SHAPE_TYPES[master]
        self.text = text
        self.pos = []
        self.size = SHAPE_SIZE[master]
        self.to_s: [Shape] = []
        self.from_s: Shape = from_s
        self.shape_type = shape_type
        self.cords = cords
        self.shapes: [Shape] = shapes
        self.flag_end = flag_end
        self.connector_text = ''

    def set_position(self, x, y) -> []:
        self.pos = [x, y]

    def move(self, vector, direction=''):
        if self.shape_type == "base":
            return

        if vector == 'r':
            self.pos[0] += 1.5

        if vector == 'l':
            self.pos[0] -= 1.5

        if vector == 'or':
            self.pos[0] += 1.5

        for i in self.shapes:
            i: Shape
            if self.pos == i.pos and self != i:
                i.move(vector)

        if not direction or direction == 'd':
            for i in self.to_s:
                i.move(vector, 'd')
        if not direction or direction == 'u':
            self.from_s.move(vector, 'u')

    def get_xml(self) -> str:
        return f"""<Shape ID='{self.shape_id}' Type='Shape' Master='{self.master}'><Cell N='PinX' V='{self.pos[0]}'/>
        <Cell N='PinY' V='{self.pos[1]}'/>
        <Text>{self.text}</Text></Shape>
        """
