import parser
from visio import shape, lxml
from visio.vsdx import Vsdx

v = Vsdx("new.vsdx")
lx = lxml.Lxml()

last = lx.add_shape('START', 'Начало', 'd')


def draw(string, last, vector='d', ifka=False, flag_end=False):
    emp = string.replace(' ', '').replace(';', '').replace('}', '').replace('{', '')
    if ifka:
        last = lx.add_shape('IF', p.final_transformation(string), vector, last)
    elif p.parse_variable_initializations(string):
        temp = []
        for i in p.parse_variable_initializations(string):
            temp.append(f'{p.final_transformation(str(i[0]))} = {p.final_transformation(str(i[1]))}')
        last = lx.add_shape('PROCESS', p.final_transformation('\n'.join(temp)), vector, last, flag_end)
    elif p.parse_io(string):
        last = lx.add_shape('INPUT', p.final_transformation(p.parse_io(string)), vector, last, flag_end)
    elif p.parse_while(string):
        last = lx.add_shape('IF', p.final_transformation(p.parse_while(string)), vector, last, flag_end)
    elif p.parse_for(string):
        last = lx.add_shape('MODIFICATION', p.final_transformation(p.parse_for(string)), vector, last, flag_end)
    elif not emp or emp == 'do':
        ...
    elif funk_name == 'main' and 'return 0' in string:
        ...
    else:
        last = lx.add_shape('PROCESS', p.final_transformation(string.replace(';', '').lstrip()), vector, last, flag_end)
    return last


def draw_if(ifs, vector='d'):
    global last
    deep = [1, 1]
    last = draw(ifs['Condition'], last, vector, True)
    block_if = last
    for flag in [True, False]:
        first = True
        sdvig = 0
        for i_n in range(len(ifs[flag])):
            strings = []
            if sdvig:
                sdvig -= 1
                continue

            print(ifs[flag])
            for s in range(i_n, len(ifs[flag])):
                if type(ifs[flag][s]) == dict:
                    break
                strings.append(ifs[flag][s])
            sdvig = 0
            if strings:
                print(strings)
                switch2 = p.parse_switch(0, strings)
                if switch2:
                    sdvig = switch2[1]

            i = ifs[flag][i_n]
            if type(i) == dict:
                if first:
                    last = block_if
                    deep[0 if flag else 1] += draw_if(i, vector=('r' if flag else 'l'))
                    first = False
                else:
                    deep[0 if flag else 1] += draw_if(i)
            else:
                if first:
                    if sdvig:
                        temp = draw_switch(switch2[0], 'r' if flag else 'l', last if flag else block_if)
                        last = temp[0]
                        deep[0 if flag else 1] += temp[1]
                        first = False

                    else:
                        last_t = draw(i, (last if flag else block_if), ('r' if flag else 'l'))
                        deep[0 if flag else 1] += 1
                        if last_t != last:
                            first = False
                else:
                    if sdvig:
                        temp = draw_switch(switch2[0])
                        last = temp[0]
                        deep[0 if flag else 1] += temp[1]
                    else:
                        last_t = draw(i, last)
                        if last_t != last and not sdvig:
                            deep[0 if flag else 1] += 1
                if not sdvig:
                    last = last_t

    if last.master == shape.SHAPE_TYPES['POINT']:
        deep[0] += 1
        deep[1] += 1
    x, y = block_if.pos[0], block_if.pos[1] - max(deep)
    # print(deep, block_if.text, block_if.pos, [x, y])
    last = lx.add_shape('POINT', max(deep), 'd', last, flag_end=True)
    lx.cords.remove(last.pos)
    last.set_position(x, y)
    return max(deep)


def draw_switch(switch: dict[str, dict], vector='d', last_if=None):
    global last
    depth = 0
    flag_first = True
    head_if = last = lx.add_shape("IF", switch["condition"], vector, last_if if last_if else last)
    for case in switch["cases"]:
        flag_first_case = True
        for string in switch["cases"][case]:
            if flag_first:
                head_case = last = draw(string, last, 'r')
                last.connector_text = p.replace_xml_special_symbols(case)
                flag_first = False
            else:
                last = draw(string, head_case if flag_first_case else last, 'd' if flag_first_case else 'or')
                last.connector_text = p.replace_xml_special_symbols(case)
                if flag_first_case:
                    head_case = last
            flag_first_case = False
        if head_if != last:
            depth += 1
    last = lx.add_shape('SWITCH_POINT', depth, 'l', head_case)
    lx.add_connector(head_if, head_case)
    return last, depth + 1


p = parser.Parser()
p.read('primer.cpp')
funk_name = 'main'
f_type = 'int'
p.prepare()
p.define()

# print(p.parse_defines_with_brackets)
# print(p.parse_defines_without_brackets)

p.replace_modification()
p.find_func(f_type)

# p.parse_switch(0, ['  switch (c) {', '    case 0:', '      y = sin(k / 3) + sqrt(cbrt(k + 1));', '      y = sin(k / 3) + sqrt(cbrt(k + 1));', '      break;', '    case 1:', '      y = tan(pow(k, 2)) + sqrt(k + 1);', '      break;', '    case 2:', '      y = pow(atan(k + 1), 2);', '      break;', '    case 3:', '      y = pow(E, (k + 1) / 10);', '      break;', '    default:', '      cout << "Can\'t calculate" << endl;'])

sdvig = 0

if not p.funcs.get(funk_name, False):
    print(f'Функции {funk_name} нет в коде')
    exit()

for stringn in range(len(p.funcs[funk_name])):
    if sdvig:
        if sdvig != stringn:
            continue
        else:
            sdvig = 0

    string: str = p.funcs[funk_name][stringn]

    ifs = p.parse_if(stringn, p.funcs[funk_name])
    if ifs[0][True] or ifs[0][False]:
        sdvig = ifs[1]
        draw_if(ifs[0])
        continue
    switch = p.parse_switch(stringn, p.funcs[funk_name])
    if switch:
        sdvig = switch[1]
        draw_switch(switch[0])
        continue

    last = draw(string, last)

lx.add_shape('START', 'Конец', 'd', last)

lx.write_file()
v.save_vsdx_file()
