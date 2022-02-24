from communication_grid import Grid
from genetic_pgcs import GeneticPGCSOptimizer
from evaluation_cost import *

input_f = "small_entry.txt"
cost_f = "input_cost.txt"

#New genetic optimizer
genopti = GeneticPGCSOptimizer(input_f,pop_size = 10,gen_number = 50,select_number = 5)
optimal_grid = genopti.genetic_algorithm()
optimal_grid.display()


