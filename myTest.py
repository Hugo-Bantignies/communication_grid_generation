from communication_grid import Grid
from evaluation_cost import *

input_f = "small_entry.txt"
cost_f = "input_cost.txt"
r_size = 5
c_size = 5

gtest = Grid(input_f,r_size,c_size,"accueil",randomizer = True)

print("Cost of the grid gtest : " + str(grid_cost(gtest,cost_f)))

