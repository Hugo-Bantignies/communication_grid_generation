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
import random
from utils import *

source_f = "input_corpora/animal_proof_3.txt"
eval_f = "input_evaluation/animal_proof_3.txt"

def pgcs_crossover_swap(g_a, g_b):

      voc_x = g_a.get_core_voc()
      voc_y = g_b.get_core_voc()

      list_voc_x = []
      list_voc_y = []
      identifiers = []

      for picto_x in voc_x.values():
        list_voc_x.append(picto_x)

      for picto_y in voc_y.values():
        list_voc_y.append(picto_y)

      for slot_y in range(len(list_voc_y)):

        if(random.random() < 0.5):

          target_word = list_voc_y[slot_y][0]
          new_row = list_voc_y[slot_y][1]
          new_col = list_voc_y[slot_y][2]

          i = 0
          for picto in list_voc_x:
            if(picto[0] == target_word):

              target_row = picto[1]
              target_col = picto[2]
              target_save = picto
              slot_x = i

            if(picto[1] == new_row and picto[2] == new_col):

              picto_save = picto

            i = i + 1
    
          picto_save[1] = target_row
          picto_save[2] = target_col
          target_save[1] = new_row
          target_save[2] = new_col

          list_voc_x[slot_x] = picto_save
          list_voc_x[slot_y] = target_save

          list_voc_x[slot_x], list_voc_x[slot_y] = list_voc_x[slot_y], list_voc_x[slot_x]

      for picto in list_voc_x:
        identifiers.append(picto[4])

      new_voc = dict(zip(identifiers,list_voc_x))

      new_ind = Grid(new_voc)

      return new_ind,new_ind

def pgcs_mutation_swap(g):

      voc = g.get_core_voc()

      list_voc = []
      identifiers = []

      for picto in voc.values():
        list_voc.append(picto)
      
      slot_a = random.randint(0,len(list_voc) - 1)
      slot_b = random.randint(0,len(list_voc) - 1)

      tmp_a = (list_voc[slot_a][0], list_voc[slot_a][1],list_voc[slot_a][2], list_voc[slot_a][3], list_voc[slot_a][4])


      list_voc[slot_a][0] = list_voc[slot_b][0]
      list_voc[slot_a][3] = list_voc[slot_b][3]
      list_voc[slot_a][4] = list_voc[slot_b][4]

      list_voc[slot_b][0] = tmp_a[0]
      list_voc[slot_b][3] = tmp_a[3]
      list_voc[slot_b][4] = tmp_a[4]

      #list_voc[slot_a], list_voc[slot_b] = list_voc[slot_b], list_voc[slot_a]

      for picto in list_voc:
        identifiers.append(picto[4])

      new_voc = dict(zip(identifiers,list_voc))

      new_ind = Grid(new_voc)

      return new_ind


new_voc = dict()
g = Grid(source_f,randomizer = False)
g.display()
print(str(g))
    

for i in range(10):
    gnew = pgcs_mutation_swap(g)
    gnew.display()

    print("CROSSOVER")
    g_end,g_bis = pgcs_crossover_swap(g,gnew)
    print(str(g_end))

    for picto in g_end.get_core_voc().values():
        print(picto)
