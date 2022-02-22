from communication_grid import Grid
from evaluation_cost import *

input_f = "small_entry.txt"
cost_f = "input_cost.txt"

gtest_a = Grid(input_f,"accueil",randomizer = True,dynamic_size = True)
gtest_b = Grid(input_f,"accueil",randomizer = False,dynamic_size = True)

gtest_a.display()

print("Cost of the grid gtest (random) : " + str(grid_cost(gtest_a,cost_f)))
print("Cost of the grid gtest (not random) : " + str(grid_cost(gtest_b,cost_f)))


