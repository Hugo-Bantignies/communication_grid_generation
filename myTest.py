from communication_grid import Pictogram
from communication_grid import Slot
from communication_grid import Page
from communication_grid import Grid

input_f = "small_entry.txt"
r_size = 5
c_size = 5

gtest = Grid(input_f,r_size,c_size,"accueil")
gtest.display()