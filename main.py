import parser
from visio import shape, lxml
from visio.vsdx import Vsdx


v = Vsdx("new.vsdx")
lx = lxml.Lxml()


last = lx.add_shape('START', 'Начало', 'd')


def draw(string, last, vector='d', ifka=False):
    emp = string.replace(' ', '').replace(';', '').replace('}', '').replace('{', '')
    if ifka:
        last = lx.add_shape('IF', p.final_transformation(string), vector, last)
    elif p.parse_variable_initializations(string):
        temp = []
        for i in p.parse_variable_initializations(string):
            temp.append(f'{p.final_transformation(str(i[0]))} = {p.final_transformation(str(i[1]))}')
        last = lx.add_shape('PROCESS', p.final_transformation('\n'.join(temp)), vector, last)
    elif p.parse_io(string):
        last = lx.add_shape('INPUT', p.final_transformation(p.parse_io(string)), vector, last)
    elif p.parse_while(string):
        last = lx.add_shape('IF', p.final_transformation(p.parse_while(string)), vector, last)
    elif p.parse_for(string):
        last = lx.add_shape('MODIFICATION', p.final_transformation(p.parse_for(string)), vector, last)
    elif not emp or emp == 'do':
        ...
    elif funk_name == 'main' and 'return 0' in string:
        ...
    else:
        last = lx.add_shape('PROCESS', p.final_transformation(string.replace(';', '').lstrip()), vector, last)
    return last


def draw_if(ifs, vector='d'):
    global last
    deep = [1, 1]
    last = draw(ifs['Condition'], last, vector, True)
    block_if = last
    for flag in [True, False]:
        first = True
        for i in ifs[flag]:
            if type(i) == dict:
                if first:
                    last = block_if
                    deep[0 if flag else 1] += draw_if(i, vector=('r' if flag else 'l'))
                    first = False
                else:
                    deep[0 if flag else 1] += draw_if(i)
            else:
                if first:
                    last_t = draw(i, (last if flag else block_if), ('r' if flag else 'l'))
                    if last_t != last:
                        first = False
                else:
                    last_t = draw(i, last)
                if last_t != last:
                    deep[0 if flag else 1] += 1
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

    last = draw(string, last)

lx.add_shape('START', 'Конец', 'd', last)

lx.write_file()
v.save_vsdx_file()
