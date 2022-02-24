from typing import Text
from GeneticPGCSOptimizer import GeneticPGCSOptimizer
from text_generator import TextGenerator

input_f = "small_entry.txt"
cost_f = "input_cost.txt"


#Generation of the cost file input
textgen = TextGenerator(source_file = input_f,sentence_number=100,sentence_length=5)
textgen.generation()

#New genetic optimizer
genopti = GeneticPGCSOptimizer(input_f,pop_size = 10,gen_number = 50,select_number = 5,randomizer = False)
optimal_grid = genopti.genetic_algorithm()
optimal_grid.display()


