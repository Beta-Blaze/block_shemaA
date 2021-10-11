import random

CONNECTOR_WIDTH = 0.25


class Connector:
    def __init__(self, shape_from, shape_to, ):
        """
        :param shape_from: Shape object
        :param shape_to: Shape object
        """
        self.from_id = shape_from.id
        self.to_id = shape_to.id
        self.begin_x = shape_from.pos[0]
        self.begin_y = shape_from.pos[1]
        self.end_x = shape_to.pos[0]
        self.end_y = shape_to.pos[0]
        self.height = self.end_y - self.begin_y

    def get_xml(self):
        return f"""<Shape ID='{random.randint(2000, 30000)}' Type='Shape' Master='20'>
                        <Cell N='PinX' V='{self.begin_x}'/>
                        <Cell N='PinY' V='{self.begin_y}'/>
                        <Cell N='Width' F='GUARD({CONNECTOR_WIDTH}DL)'/>
                        <Cell N='LocPinX' V='{CONNECTOR_WIDTH * 0.5}'/>
                        <Cell N='Height' F='GUARD(EndY-BeginY)'/>
                        <Cell N='LocPinY' V='{(self.end_y - self.begin_y) * 0.5}'/>
                        <Cell N='BeginX' V='{self.begin_x}' />
                        <Cell N='BeginY' V='{self.begin_y}' />
                        <Cell N='EndX' V='{self.end_x}' />
                        <Cell N='EndY' V='{self.end_y}' />
                        <Cell N='TxtPinX' V='0.125'/>
                        <Cell N='TxtPinY' V='-0.4281495809555054'/>
                        <Section N='Control'>
                            <Row N='TextPosition'>
                                <Cell N='X' V='{CONNECTOR_WIDTH * 0.5}'/>
                                <Cell N='Y' V='{(self.end_y - self.begin_y) * 0.5}'/>
                                <Cell N='XDyn' V='{CONNECTOR_WIDTH * 0.5}' />
                                <Cell N='YDyn' V='{(self.end_y - self.begin_y) * 0.5}' />
                            </Row>
                        </Section>
                        <Section N='Geometry' IX='0'>
                            <Row T='MoveTo' IX='1'> <Cell N='X' V='{CONNECTOR_WIDTH * 0.5}'/></Row>
                            <Row T='LineTo' IX='2'><Cell N='X' V='{CONNECTOR_WIDTH * 0.5}'/>
                                <Cell N='Y' V='{(self.end_y - self.begin_y) * 0.1}'/>
                            </Row>
                            <Row T='LineTo' IX='3' Del='1'/>
                        </Section>
                    </Shape>
        """
