from shape import id_shape_counter
CONNECTOR_WIDTH = 0.25


class Connector:
    def __init__(self, shape_from, shape_to, connector_position):
        """
        :param shape_from: Shape object
        :param connector_position: true - vertical; false - horizontal
        :param shape_to: Shape object
        """
        self.shape_from = shape_from
        self.shape_to = shape_to
        self.connector_position = connector_position
        self.begin_x = self.begin_y = self.end_y = self.end_x = \
            self.height = self.pin_x = self.pin_y = None

    def calculate_position(self):
        self.begin_x = self.shape_from.pos[0] if self.connector_position[0] else self.shape_from.pos[1] - self.shape_from.size[0] / 2
        self.begin_y = self.shape_from.pos[1] - self.shape_from.size[0] / 2 if self.connector_position[0] else self.shape_from.pos[1]
        self.end_x = self.shape_to.pos[0] if self.connector_position[1] else self.shape_to.pos[1] + self.shape_to.size[0] / 2
        self.end_y = self.shape_to.pos[1] + self.shape_to.size[0] / 2 if self.connector_position[1] else self.shape_to.pos[1]
        self.height = self.end_y - self.begin_y
        self.pin_x = self.begin_x if self.connector_position[0] else self.shape_from.pos[0] - (self.shape_from.pos[0] - self.shape_to.pos[0]) / 2
        self.pin_y = self.shape_from.pos[1] - (self.shape_from.pos[1] - self.shape_to.pos[1]) / 2 if self.connector_position[0] else self.begin_y

    def get_xml(self):
        global id_shape_counter
        id_shape_counter += 1
        return f"""<Shape ID='{id_shape_counter}' Type='Shape' Master='11'>
                        <Cell N='PinX' V='{self.pin_x}'/>
                        <Cell N='PinY' V='{self.pin_y}'/>
                        <Cell N='Width' F='GUARD({CONNECTOR_WIDTH}DL)'/>
                        <Cell N='Height' V = '{self.height}' F='GUARD(EndY-BeginY)'/>
                        <Cell N='LocPinX' V='{CONNECTOR_WIDTH * 0.5}'/>
                        <Cell N='LocPinY' V='{self.height * 0.5}'/>
                        <Cell N='BeginX' V='{self.begin_x}' />
                        <Cell N='BeginY' V='{self.begin_y}' />
                        <Cell N='EndX' V='{self.end_x}' />
                        <Cell N='EndY' V='{self.end_y}' />
                        <Cell N='TxtPinX' V='0.125'/>
                        <Cell N='TxtPinY' V='-0.4281495809555054'/>
                        <Section N='Control'>
                            <Row N='TextPosition'>
                                <Cell N='X' V='{CONNECTOR_WIDTH * 0.5}'/>
                                <Cell N='Y' V='{self.height * 0.5}'/>
                                <Cell N='XDyn' V='{CONNECTOR_WIDTH * 0.5}' />
                                <Cell N='YDyn' V='{self.height * 0.5}' />
                            </Row>
                        </Section>
                        <Section N='Geometry' IX='0'>
                            <Row T='MoveTo' IX='1'> 
                                <Cell N='X' V='{CONNECTOR_WIDTH * 0.5}'/></Row>
                            <Row T='LineTo' IX='2'>
                                <Cell N='X' V='{CONNECTOR_WIDTH * 0.5}'/>
                                <Cell N='Y' V='{self.height}'/>
                            </Row>
                            <Row T='LineTo' IX='3' Del='1'/>
                        </Section>
                    </Shape>
        """
