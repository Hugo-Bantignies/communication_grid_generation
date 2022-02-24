from typing import Text
from GeneticPGCSOptimizer import GeneticPGCSOptimizer
from text_generator import TextGenerator

source_f = "small_entry.txt"
eval_f = "input_cost.txt"


#Generation of the cost file input
textgen = TextGenerator(source_file = source_f,sentence_number=100,sentence_length=5)
textgen.generation()

#New genetic optimizer
genopti = GeneticPGCSOptimizer(source_f,eval_f,pop_size = 100,gen_number = 100,select_number = 20,randomizer = False)
optimal_grid = genopti.genetic_algorithm()
optimal_grid.display()


