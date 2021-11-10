from cpp2visio import parser
from cpp2visio.drawer import Drawer
from visio import lxml
from visio.vsdx import Vsdx

v = Vsdx("new.vsdx")
lx = lxml.Lxml()
p = parser.Parser()
p.read('primer.cpp')
funk_name = 'main'
f_type = 'int'
p.prepare()
p.define()

p.replace_modification()
p.find_func(f_type)

sdvig = 0

if not p.funcs.get(funk_name, False):
    print(f'Функции {funk_name} нет в коде')
    exit()

d = Drawer(p, funk_name)

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
        d.draw_if(ifs[0])
        continue
    switch = p.parse_switch(stringn, p.funcs[funk_name])
    if switch:
        sdvig = switch[1]
        d.draw_switch(switch[0])
        continue

    d.process_line(string)

d.drawww()
v.save_vsdx_file()
