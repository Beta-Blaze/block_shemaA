from vsdx import Vsdx
from lxml import Lxml
from shape import Shape

v = Vsdx("new.vsdx")

lx = Lxml()
my_shape1 = lx.add_shape(Shape("PROCESS", "1"), 'd')
my_shape2 = lx.add_shape(Shape("PROCESS", "2"), 'r', my_shape1)
my_shape3 = lx.add_shape(Shape("PROCESS", "3"), 'l', my_shape1)
my_shape4 = lx.add_shape(Shape("PROCESS", "4"), 'd', my_shape2)
my_shape5 = lx.add_shape(Shape("PROCESS", "5"), 'd', my_shape3)

my_shape = lx.add_shape(Shape("PROCESS", "6"), 'r', my_shape5)
my_shape = lx.add_shape(Shape("PROCESS", "7"), 'l', my_shape4)

lx.write_file()

v.save_vsdx_file()
