from visio import lxml, shape


class Drawer:

    def __init__(self, p, funk_name):
        self.lx = lxml.Lxml()
        self.p = p
        self.funk_name = funk_name
        self.last = self.lx.add_shape('START', 'Начало', 'd')

    def draw(self, string, last=None, vector='d', ifka=False, flag_end=False):
        if not last:
            last = self.last
        emp = string.replace(' ', '').replace(';', '').replace('}', '').replace('{', '')
        if ifka:
            last = self.lx.add_shape('IF', self.p.final_transformation(string), vector, last)
        elif self.p.parse_variable_initializations(string):
            temp = []
            for i in self.p.parse_variable_initializations(string):
                temp.append(f'{self.p.final_transformation(str(i[0]))} = {self.p.final_transformation(str(i[1]))}')
            last = self.lx.add_shape('PROCESS', self.p.final_transformation('\n'.join(temp)), vector, last, flag_end)
        elif self.p.parse_io(string):
            last = self.lx.add_shape('INPUT', self.p.final_transformation(self.p.parse_io(string)), vector, last, flag_end)
        elif self.p.parse_while(string):
            last = self.lx.add_shape('IF', self.p.final_transformation(self.p.parse_while(string)), vector, last, flag_end)
        elif self.p.parse_for(string):
            last = self.lx.add_shape('MODIFICATION', self.p.final_transformation(self.p.parse_for(string)), vector, last, flag_end)
        elif not emp or emp == 'do':
            ...
        elif self.funk_name == 'main' and 'return 0' in string:
            ...
        else:
            last = self.lx.add_shape('PROCESS', self.p.final_transformation(string.replace(';', '').lstrip()), vector, last, flag_end)
        return last

    def draw_if(self, ifs, vector='d'):
        deep = [1, 1]
        self.last = self.draw(ifs['Condition'], self.last, vector, True)
        block_if = self.last
        for flag in [True, False]:
            first = True
            sdvig = 0
            for i_n in range(len(ifs[flag])):
                strings = []
                if sdvig:
                    sdvig -= 1
                    continue

                for s in range(i_n, len(ifs[flag])):
                    if type(ifs[flag][s]) == dict:
                        break
                    strings.append(ifs[flag][s])
                sdvig = 0
                if strings:
                    switch2 = self.p.parse_switch(0, strings)
                    if switch2:
                        sdvig = switch2[1]

                i = ifs[flag][i_n]
                if type(i) == dict:
                    if first:
                        self.last = block_if
                        deep[0 if flag else 1] += self.draw_if(i, vector=('r' if flag else 'l'))
                        first = False
                    else:
                        deep[0 if flag else 1] += self.draw_if(i)
                else:
                    if first:
                        if sdvig:
                            switch_deep = self.draw_switch(switch2[0], 'r' if flag else 'l', self.last if flag else block_if)
                            deep[0 if flag else 1] += switch_deep
                            first = False

                        else:
                            last_t = self.draw(i, (self.last if flag else block_if), ('r' if flag else 'l'))
                            if last_t != self.last:
                                first = False
                            deep[0 if flag else 1] += 1
                    else:
                        if sdvig:
                            switch_deep = self.draw_switch(switch2[0])
                            deep[0 if flag else 1] += switch_deep[1]
                        else:
                            last_t = self.draw(i, self.last)
                            if last_t != self.last and not sdvig:
                                deep[0 if flag else 1] += 1
                    if not sdvig:
                        self.last = last_t

        x, y = block_if.pos[0], block_if.pos[1] - max(deep)
        self.last = self.lx.add_shape('POINT', max(deep), 'd', self.last, flag_end=True)
        self.lx.cords.remove(self.last.pos)
        self.last.set_position(x, y)
        deep = map(lambda d: d + 1, deep)
        return max(deep)

    def draw_switch(self, switch: dict[str, dict], vector='d', last_if=None):
        depth = 0
        flag_first = True
        head_if = self.last = self.lx.add_shape("IF", switch["condition"], vector, last_if if last_if else self.last)
        for case in switch["cases"]:
            flag_first_case = True
            for string in switch["cases"][case]:
                if flag_first:
                    head_case = self.last = self.draw(string, self.last, 'r')
                    self.last.connector_text = self.p.replace_xml_special_symbols(case)
                    flag_first = False
                else:
                    self.last = self.draw(string, head_case if flag_first_case else self.last, 'd' if flag_first_case else 'or')
                    self.last.connector_text = self.p.replace_xml_special_symbols(case)
                    if flag_first_case:
                        head_case = self.last
                flag_first_case = False
            if head_if != self.last:
                depth += 1
        self.last = self.lx.add_shape('SWITCH_POINT', depth, 'l', head_case)
        self.lx.add_connector(head_if, head_case)
        return depth + 1

    def process_line(self, line):
        self.last = self.draw(line)

    def finish_drawing(self):
        self.lx.add_shape('START', 'Конец', 'd', self.last)
        self.lx.write_file()
