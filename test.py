from communication_grid import Grid
from evaluation_cost import *

g = Grid("default.csv")
g.display_information()
g.naive_cut(20,24)
g.to_csv()
