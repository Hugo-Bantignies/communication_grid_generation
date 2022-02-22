from communication_grid import Grid
from evaluation_cost import *

input_f = "small_entry.txt"
cost_f = "input_cost.txt"
r_size = 5
c_size = 5

gtest_a = Grid(input_f,r_size,c_size,"accueil",True)
gtest_b = Grid(input_f,r_size,c_size,"accueil",True)

print("Cost of the grid gtest_a : " + str(grid_cost(gtest_a,cost_f)))
print("Cost of the grid gtest_b : " + str(grid_cost(gtest_b,cost_f)))

