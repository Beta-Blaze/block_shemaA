import vsdx, lxml, shape, connector, parser, re


# def replace_define(string: str, p: parser.Parser()):
#     for i in p.parse_defines_with_brackets:
#         inits = re.finditer(r".*?{}\((.+?)\)".format(i), string)
#         for init in inits:
#             perem = init.group(1)
#             string = string.replace(f'{i}({perem})', perem.join(p.parse_defines_with_brackets[i]))
#     return string

v = vsdx.Vsdx("new.vsdx")
lx = lxml.Lxml()


last = lx.add_shape('START', 'Начало', 'd')


def draw(string, last, vector='d'):
    emp = string.replace(' ', '').replace(';', '').replace('}', '').replace('{', '')
    if p.parse_variable_initializations(string):
        temp = []
        for i in p.parse_variable_initializations(string):
                temp.append(f'{i[0]} = {i[1]}')
        last = lx.add_shape('PROCESS', '&#xA;'.join(temp), vector, last)
    elif p.parse_io(string):
        last = lx.add_shape('INPUT', p.parse_io(string), vector, last)
    elif p.parse_while(string):
        last = lx.add_shape('IF',  p.parse_while(string), vector, last)
    elif p.parse_for(string):
        last = lx.add_shape('MODIFICATION',  p.parse_for(string), vector, last)
    elif not emp or emp == 'do':
        ...
    else:
        last = lx.add_shape('PROCESS', string.replace(';', '').lstrip(), vector, last)
    return last


def draw_if(ifs, vector='d'):
    global last
    deep = [0, 0]
    last = lx.add_shape('IF', ifs['Condition'], vector, last)
    block_if = last
    for flag in [True, False]:
        first = True
        for i in ifs[flag]:
            if type(i) == dict:
                if first:
                    deep[0 if flag else 1] += draw_if(i, vector=('r' if flag else 'l'))
                    first = False
                else:
                    deep[0 if flag else 1] += draw_if(i)
            else:
                if first:
                    last = draw(i, (last if flag else block_if), ('r' if flag else 'l'))
                    first = False
                else:
                    last = draw(i, last)
            deep[0 if flag else 1] += 1

    x, y = block_if.pos[0], block_if.pos[1] - max(deep)
    last = lx.add_shape('INPUT', 'QWE', vector, last)
    print(max(deep), ifs)
    last.set_position(x, y)
    return max(deep)


p = parser.Parser()
p.read('primer.cpp')
p.prepare()
p.define()

# print(p.parse_defines_with_brackets)
# print(p.parse_defines_without_brackets)

p.replace_modification()
p.find_func()

sdvig = 0

for stringn in range(len(p.funcs['main'])):
    if sdvig:
        if sdvig != stringn:
            continue
        else:
            sdvig = 0
    string: str = p.funcs['main'][stringn]

    ifs = p.parse_if(stringn, p.funcs['main'])
    if ifs[0][True] or ifs[0][False]:
        sdvig = ifs[1]
        draw_if(ifs[0])
        continue

    last = draw(string, last)

lx.add_shape('START', 'Конец', 'd', last)

lx.write_file()
v.save_vsdx_file()
