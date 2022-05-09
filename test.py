from PictogramGrid import Pictogram,Page,Grid
from EvaluationGrid import grid_distance_cost,sentence_distance_cost
from gpgo import gpgo
import os
import random

corpus = []

for root, dirs, files in os.walk("training_corpora"):
    for name in files:
        corpus.append(os.path.join(root,name))

'''my_gpgo= gpgo(corpus,corpus,pop_size=2,cross_proba=1,cross_info_rate=1,
              mutation_proba=0,select_number=2,gen_number=1,randomizer=True)

my_gpgo.display_config()

g = my_gpgo.genetic_algorithm()'''

g = Grid(corpus,randomizer=False,warnings = False,page_row_size=5,page_col_size=5)
for p in g.pages.values():
    print(p)
cost = sentence_distance_cost(g,"observe chat".split(" "))
print(cost)

'''g = Grid(corpus,randomizer=False,warnings = False)
picto_a = g.pages["accueil"].pictograms["chien"]
picto_b = g.pages["default0"].pictograms["singe"]

g.swap_pictograms(picto_a,picto_b)

picto_a = g.pages["default0"].pictograms["chien"]
picto_b = g.pages["default1"].pictograms["feuilles"]

g.swap_pictograms(picto_a,picto_b)

for p in g.pages.values():
    print(p)'''