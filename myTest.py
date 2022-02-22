from communication_grid import Grid
from genetic_pgcs import GeneticPGCSOptimizer
from evaluation_cost import *

input_f = "small_entry.txt"
cost_f = "input_cost.txt"

#New grid (generate from an input file)
gtest = Grid(input_f,"accueil",randomizer = True, dynamic_size = True)
#Display the grid
gtest.display()

#Cost computation
print("Cost of the grid gtest (random) : " + str(grid_cost(gtest,cost_f)))

#New genetic optimizer
genopti = GeneticPGCSOptimizer(gtest)



