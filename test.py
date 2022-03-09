#!python -m pip install networkx
#!python -m pip install matplotlib==2.2.3
#!python -m pip install ipywidgets
#!python -m pip install graphviz
#!python -m pip install pandas
#!python -m pip install pudb
#!python -m pip install nbconvert
#!python -m pip install nbconvert -U
#coding=utf-8

import GeneticPGCSOptimizer as go
from communication_grid import Grid
import matplotlib.pyplot as plt
from utils import *

source_f = "training_corpora/animals_corpus.txt"
eval_f = "evaluation_corpora/animals_eval.txt"

if __name__ == '__main__':
    optimizer = go.GeneticPGCSOptimizer(source_f,eval_f,pop_size = 150, select_number = 30,
                                           gen_number = 100, randomizer = True, distance_formula = "euclidean",
                                           cost_average = False)

    optimal_grid,cost,best_hist = optimizer.genetic_pgcs_optimization()

    print("\n BEST COST : ",cost)
    optimal_grid.display()