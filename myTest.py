from GeneticPGCSOptimizer import GeneticPGCSOptimizer
import matplotlib.pyplot as plt

source_f = "input_corpora/animals_corpus.txt"
eval_f = "input_evaluation/animals_eval.txt"

#New genetic optimizer
genopti = GeneticPGCSOptimizer(source_f,eval_f,pop_size = 20,gen_number = 10,select_number = 5,randomizer = True,cross_proba = 0.5, mutation_proba = 0.5)
optimal_grid = genopti.genetic_algorithm()
history  = genopti.fitness_history(option="best")


optimal_grid.display()
plt.plot(history)
plt.show()

