from typing import Text
from GeneticPGCSOptimizer import GeneticPGCSOptimizer
from text_generator import TextGenerator
import matplotlib.pyplot as plt

source_f = "small_entry.txt"
eval_f = "input_cost.txt"

#New genetic optimizer
genopti = GeneticPGCSOptimizer(source_f,eval_f,pop_size = 100,gen_number = 100,select_number = 20,randomizer = False)
optimal_grid = genopti.genetic_algorithm()
history  = genopti.fitness_history()


optimal_grid.display()
plt.plot(history)
plt.show()

