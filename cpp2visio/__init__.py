from cpp2visio import parser
from cpp2visio.drawer import Drawer
from visio.vsdx import Vsdx

def get_funcs(f_type):
    p = parser.Parser()
    p.read('primer.cpp')
    p.find_func(f_type)
    return list(p.funcs)


def parse_function(f_type, function_name):
    v = Vsdx("new.vsdx")
    p = parser.Parser()
    p.read('primer.cpp')
    p.prepare()
    p.define()
    p.replace_modification()
    p.find_func(f_type)

    sdvig = 0
    d = Drawer(p, function_name)

    for stringn in range(len(p.funcs[function_name])):
        if sdvig:
            if sdvig != stringn:
                continue
            else:
                sdvig = 0

        string: str = p.funcs[function_name][stringn]
        ifs = p.parse_if(stringn, p.funcs[function_name])

        if ifs[0][True] or ifs[0][False]:
            sdvig = ifs[1]
            d.draw_if(ifs[0])
            continue
        switch = p.parse_switch(stringn, p.funcs[function_name])
        if switch:
            sdvig = switch[1]
            d.draw_switch(switch[0])
            continue

        d.process_line(string)

    d.finish_drawing()
    v.save_vsdx_file()
