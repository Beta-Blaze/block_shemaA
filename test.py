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

my_shape1 = lx.add_shape("START", "1", 'd')
my_shape2 = lx.add_shape("PROCESS", "2", 'l', my_shape1)
my_shape3 = lx.add_shape("INPUT", "3", 'd', my_shape2)
my_shape4 = lx.add_shape("IF", "4", 'd', my_shape3)
my_shape5 = lx.add_shape("START", "1", 'd', my_shape4)
my_shape6 = lx.add_shape("MODIFICATION", "2", 'd', my_shape5)
my_shape7 = lx.add_shape("DEFINED_PROCESS", "3", 'r', my_shape6)
my_shape8 = lx.add_shape("ONE_PAGE_CONNECTOR", "4", 'r', my_shape7)
my_shape9 = lx.add_shape("MULTI_PAGE_CONNECTOR", "4", 'l', my_shape8)
my_shape10 = lx.add_shape("POINT", "4", 'l', my_shape9)

lx.write_file()

v.save_vsdx_file()
