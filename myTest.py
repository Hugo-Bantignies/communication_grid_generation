from communication_grid import Pictogram
from communication_grid import Slot
from communication_grid import Grid

input_f = "small_entry.txt"
r_size = 5
c_size = 5

pict = Pictogram("chat",0,0,"accueil","chat@accueil")
slot = Slot(pict,True,None)

print(slot.__str__())


#gtest = Grid(input_f,r_size,c_size,"monAccueil")
#gtest.display()