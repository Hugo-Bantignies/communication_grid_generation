from typing import Text
from GeneticPGCSOptimizer import GeneticPGCSOptimizer
import matplotlib.pyplot as plt

source_f = "small_entry.txt"
eval_f = "input_cost.txt"

#New genetic optimizer
genopti = GeneticPGCSOptimizer(source_f,eval_f,pop_size = 500,gen_number = 200,select_number = 75,randomizer = True)
optimal_grid = genopti.genetic_algorithm()
history  = genopti.fitness_history()


optimal_grid.display()
plt.plot(history)
plt.show()

