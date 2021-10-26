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
        if self.shape_to.shape_type == 'l':
            self.begin_x = self.shape_from.pos[0] - self.shape_from.size[1] / 2
            self.begin_y = self.shape_from.pos[1]
        elif self.shape_to.shape_type == 'r':
            self.begin_x = self.shape_from.pos[0] + self.shape_from.size[1] / 2
            self.begin_y = self.shape_from.pos[1]
        elif self.shape_to.shape_type in ['d', 'base']:
            self.begin_x = self.shape_from.pos[0]
            self.begin_y = self.shape_from.pos[1] - self.shape_from.size[0] / 2
        self.end_x = self.shape_to.pos[0]
        self.end_y = self.shape_to.pos[1] + self.shape_to.size[0] / 2
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
                            </Section>
                            """ if self.shape_to.shape_type in ['r', 'l'] else f"""<Section N='Geometry' IX='0'>
                                                                                        <Row T='MoveTo' IX='1'>
                                                                                            <Cell N='X' V='{self.width * 0.5}'/>
                                                                                        </Row>
                                                                                        <Row T='LineTo' IX='2'>
                                                                                            <Cell N='X' V='{self.width * 0.5}'/>
                                                                                            <Cell N='Y' V='{self.height}'/>
                                                                                        </Row>
                                                                                        <Row T='LineTo' IX='3' Del='1'/>
                                                                                    </Section>"""

    def get_xml(self) -> str:
        if self.shape_from.flag_end or self.shape_to.flag_end or self.shape_to.shape_type == 'or':
            return ""
        self.calculate_position()
        return f"""<Shape ID='{self.shape_id}' Type='Shape' Master='13'>
                        <Cell N='PinX' V='{self.pin_x}'/>
                        <Cell N='PinY' V='{self.pin_y}'/>
                        <Cell N='Width' V='{self.width}'/>
                        <Cell N='Height' V = '{self.height}' F='GUARD(EndY-BeginY)'/>
                        <Cell N='LocPinX' V='{self.width * 0.5}'/>
                        <Cell N='LocPinY' V='{self.height * 0.5}'/>
                        <Cell N='BeginX' V='{self.begin_x}' />
                        <Cell N='BeginY' V='{self.begin_y}' />
                        <Cell N='EndX' V='{self.end_x}' />
                        <Cell N='EndY' V='{self.end_y}' />
                        <Cell N='TxtPinX' V='0.125'/>
                        <Cell N='TxtPinY' V='-0.4281495809555054'/>
                        <Section N='Control'>
                            <Row N='TextPosition'>
                                <Cell N='X' V='{self.width * 0.5}'/>
                                <Cell N='Y' V='{self.height * 0.5}'/>
                                <Cell N='XDyn' V='{self.width * 0.5}' />
                                <Cell N='YDyn' V='{self.height * 0.5}' />
                            </Row>
                        </Section>
                        {self.geometry}
                    </Shape>
        """
