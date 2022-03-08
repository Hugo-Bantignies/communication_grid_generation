#!python -m pip install networkx
#!python -m pip install matplotlib==2.2.3
#!python -m pip install ipywidgets
#!python -m pip install graphviz
#!python -m pip install pandas
#!python -m pip install pudb
#!python -m pip install nbconvert
#!python -m pip install nbconvert -U
#coding=utf-8

from random import random
import GeneticPGCSOptimizer as go
from communication_grid import Grid
import matplotlib.pyplot as plt
from utils import *

source_f = "training_corpora/animals_corpus.txt"
eval_f = "evaluation_corpora/animals_eval.txt"

if __name__ == '__main__':
    g,cost = go.multiproc_genetic_pgcs_optimization(source_f,eval_f,pop_size = 100, select_number = 30,
                                           gen_number = 200, randomizer = True, distance_formula = "euclidean",
                                           cost_average = False)

    print("Best cost : ",cost)
    g.display()