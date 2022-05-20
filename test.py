from PictogramGrid import Pictogram,Page,Grid
from EvaluationGrid import grid_distance_cost,sentence_distance_cost,grid_cost
from gpgo import gpgo
import os
import random

corpus = []
input_grid_file = "default.csv"

for root, dirs, files in os.walk("training_corpora"):
    for name in files:
        corpus.append(os.path.join(root,name))

g = Grid(corpus,randomizer=False,warnings=True)

picto_a = g.pages["accueil"].pictograms["default1"]
picto_b = g.pages["default2"].pictograms["toucan"]

c = grid_cost(g,corpus,None,0)

g.swap_pictograms(picto_a,picto_b)

c = grid_cost(g,corpus,None,0)

print(c)