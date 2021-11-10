from visio import shape


class Connector:
    def __init__(self, shape_id, shape_from: shape.Shape, shape_to: shape.Shape):
        """
        :param shape_from: Shape object
        :param shape_to: Shape object
        """
        self.shape_from = shape_from
        self.shape_to = shape_to
        self.shape_id = shape_id
        self.begin_x = self.begin_y = self.end_y = self.end_x = self.height = self.width = self.pin_x = self.pin_y = self.geometry = None

    def calculate_position(self):
        def get_connection_point(_shape: shape.Shape, connection_point):
            match connection_point:
                case "U":
                    return _shape.pos[0], _shape.pos[1] + _shape.size[1] / 2
                case "R":
                    return _shape.pos[0] + _shape.size[0] / 2, _shape.pos[1]
                case "L":
                    return _shape.pos[0] - _shape.size[0] / 2, _shape.pos[1]
                case "D":
                    return _shape.pos[0], _shape.pos[1] - _shape.size[1] / 2
                case _:
                    print("Invalid connection point")
                    raise Exception

        if self.shape_to.connector_text or self.shape_to.shape_type == "or":  # Horizontal
            self.end_x, self.end_y = get_connection_point(self.shape_to, "L")
            if self.shape_from.master == shape.SHAPE_TYPES["IF"] and self.shape_to.shape_type == "d":  # Connect head if and last case connector
                self.begin_x, self.begin_y = get_connection_point(self.shape_from, "D")
                self.shape_to.connector_text = False
                self.end_x = self.begin_x
                self.end_y = self.shape_to.pos[1]
            elif self.shape_to.shape_type == "or":
                self.begin_x, self.begin_y = get_connection_point(self.shape_from, "R")
                self.shape_to.connector_text = False
            else:
                self.begin_x = self.end_x - 0.909
                self.begin_y = self.end_y
        else:  # Vertical or angled
            if self.shape_to.shape_type in ["l", "r"]:
                self.begin_x, self.begin_y = get_connection_point(self.shape_from, self.shape_to.shape_type.upper())
                self.end_x, self.end_y = get_connection_point(self.shape_to, "U")
            elif self.shape_to.shape_type in ["d", "base"]:
                self.begin_x, self.begin_y = get_connection_point(self.shape_from, "D")
                self.end_x, self.end_y = get_connection_point(self.shape_to, "U")
        self.pin_x = (self.begin_x + self.end_x) / 2
        self.pin_y = (self.begin_y + self.end_y) / 2
        self.height = self.end_y - self.begin_y
        self.width = self.end_x - self.begin_x if self.end_x - self.begin_x else 0.25

        self.geometry = f"""<Section N='Geometry' IX='0'>
                                <Row T='LineTo' IX='2'> 
                                    <Cell N='X' V='{self.width}'/>
                                    <Cell N='Y' V='0'/>
                                </Row>
                                <Row T='LineTo' IX='3'>
                                    <Cell N='X' V='{self.width}'/>
                                    <Cell N='Y' V='{self.height}'/>
                                </Row>
                                <Row T='LineTo' IX='4' Del='1'/>
                                </Section>
                                """ if self.shape_to.shape_type in ['r', 'l', 'or'] or self.shape_to.connector_text else f"""<Section N='Geometry' IX='0'>
                                                                                            <Row T='MoveTo' IX='1'>
                                                                                                <Cell N='X' V='{self.width * 0.5}'/>
                                                                                            </Row>
                                                                                            <Row T='LineTo' IX='2'>
                                                                                                <Cell N='X' V='{self.width * 0.5}'/>
                                                                                                <Cell N='Y' V='{self.height}'/>
                                                                                            </Row>
                                                                                            <Row T='LineTo' IX='3' Del='1'/>
                                                                                            <Row T='LineTo' IX='4' Del='1'/>
                                                                                        </Section>"""

    def get_xml(self):
        if self.shape_from.flag_end or self.shape_to.flag_end or self.shape_from.master == shape.SHAPE_TYPES['SWITCH_POINT'] or self.shape_to.master == shape.SHAPE_TYPES['SWITCH_POINT']:
            return ""
        self.calculate_position()
        return f"""<Shape ID='{self.shape_id}' Type='Shape' Master='17'>
                        <Cell N='PinX' V='{self.pin_x}'/>
                        <Cell N='PinY' V='{self.pin_y}'/>
                        <Cell N='Width' V='{self.width}'/>
                        <Cell N='Height' V='{self.height}'/>
                        <Cell N='LocPinX' V='{self.width * 0.5}'/>
                        <Cell N='LocPinY' V='{self.height * 0.5}'/>
                        <Cell N='BeginX' V='{self.begin_x}' />
                        <Cell N='BeginY' V='{self.begin_y}' />
                        <Cell N='EndX' V='{self.end_x}' />
                        <Cell N='EndY' V='{self.end_y}' />
                        <Cell N='TxtPinX' V='{self.width * 0.5}'/>
                        <Cell N='TxtPinY' V='{self.height * 0.5}'/>
                        <Section N='Control'>
                            <Row N='TextPosition'>
                                <Cell N='X' V='{self.width * 0.5}'/>
                                <Cell N='Y' V='{self.height * 0.5}'/>
                                <Cell N='XDyn' V='{self.width * 0.5}' />
                                <Cell N='YDyn' V='{self.height * 0.5}' />
                                </Row>
                        </Section>
                        {self.geometry}
                        {("<Text>" + self.shape_to.connector_text + "</Text>") if self.shape_to.connector_text else ""}
                    </Shape> 
             """
