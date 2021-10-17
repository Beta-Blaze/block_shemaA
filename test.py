from vsdx import Vsdx
from lxml import Lxml

v = Vsdx("new.vsdx")

lx = Lxml()
# my_shape1 = lx.add_shape(Shape("PROCESS", "1"), 'd')
# my_shape2 = lx.add_shape(Shape("IF", "2"), 'r', my_shape1)
# my_shape3 = lx.add_shape(Shape("PROCESS", "3"), 'd', my_shape2)
# my_shape4 = lx.add_shape(Shape("PROCESS", "4"), 'd', my_shape3)
#
# my_shape5 = lx.add_shape(Shape("PROCESS", "5"), 'd', my_shape1)
# my_shape6 = lx.add_shape(Shape("PROCESS", "6"), 'd', my_shape5)
# my_shape = lx.add_shape(Shape("PROCESS", "7"), 'r', my_shape6)

my_shape1 = lx.add_shape("PROCESS", "1", 'd')
my_shape2 = lx.add_shape("PROCESS", "2", 'd', my_shape1)
my_shape3 = lx.add_shape("PROCESS", "3", 'd', my_shape2)
my_shape4 = lx.add_shape("PROCESS", "4", 'd', my_shape3)

lx.write_file()

v.save_vsdx_file()
