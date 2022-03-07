#!python -m pip install networkx
#!python -m pip install matplotlib==2.2.3
#!python -m pip install ipywidgets
#!python -m pip install graphviz
#!python -m pip install pandas
#!python -m pip install pudb
#!python -m pip install nbconvert
#!python -m pip install nbconvert -U
#coding=utf-8

from GeneticPGCSOptimizer import GeneticPGCSOptimizer
from communication_grid import Grid
import matplotlib.pyplot as plt
import multiprocessing
from utils import *

source_f = "training_corpora/lilou1_hua.txt"
eval_f = "evaluation_corpora/lilou1_hua.txt"

def optimal_grid():
    g = opti1.genetic_algorithm()
    print(g)

def launch_parallell():
    p1 = multiprocessing.Process(target=optimal_grid)
    p2 = multiprocessing.Process(target=optimal_grid)
    p1.start()
    p2.start()

    p1.join()
    p2.join()

#New genetic optimizer
opti1 = GeneticPGCSOptimizer(source_f,eval_f,pop_size = 200,gen_number = 100,select_number = 10,
                                         randomizer = True, cross_proba = 0.5, cross_info_rate = 0.5,
                                         mutation_proba = 0.5, cost_average = False, distance_formula = "euclidean")


if __name__ == '__main__':
    #Starting the genetic algorithm of our optimizer
    opti1.parallel_genetic_algorithm()