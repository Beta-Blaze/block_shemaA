from vsdx import Vsdx
from lxml import Lxml
from shape import Shape

v = Vsdx("new.vsdx")

lx = Lxml()
my_shape = lx.add_shape(Shape("PROCESS", "1"), 'd')
my_shape = lx.add_shape(Shape("INPUT", "2"), 'd', my_shape)
my_shape = lx.add_shape(Shape("INPUT", "2"), 'd', my_shape)
my_shape = lx.add_shape(Shape("INPUT", "2"), 'd', my_shape)
my_shape = lx.add_shape(Shape("INPUT", "2"), 'd', my_shape)
my_shape = lx.add_shape(Shape("INPUT", "2"), 'd', my_shape)
my_shape = lx.add_shape(Shape("INPUT", "2"), 'd', my_shape)
my_shape = lx.add_shape(Shape("INPUT", "2"), 'd', my_shape)
my_shape = lx.add_shape(Shape("INPUT", "2"), 'd', my_shape)
my_shape = lx.add_shape(Shape("INPUT", "2"), 'd', my_shape)
my_shape = lx.add_shape(Shape("INPUT", "2"), 'd', my_shape)

lx.write_file()

v.save_vsdx_file()
