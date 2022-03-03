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
from evaluation_cost import *
import matplotlib.pyplot as plt
from utils import *

source_f = "input_corpora/chat_souris_5x5_corpus.txt"
eval_f = "input_evaluation/chat_souris_eval.txt"


g = Grid(source_f,randomizer = False)
g.display()

s = ['le','oiseaux','souris','le']

c = sentence_cost(g,s,"manhattan")

print(c)
