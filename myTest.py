from communication_grid import Pictogram
from communication_grid import Slot
from communication_grid import Page
from communication_grid import Grid

input_f = "scale_entry.txt"
r_size = 6
c_size = 6

pict = Pictogram("chat",0,0,"accueil","chat@accueil")
slot = Slot(pict,True,None)
page = Page("accueil",r_size,c_size)

gtest = Grid(input_f,r_size,c_size,"home")
gtest.display()