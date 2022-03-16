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

trs_to_txt("training_corpora/lilou1_hua.trs")