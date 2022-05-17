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

print(g.pages["accueil"])
g.pages["accueil"].remove_pictogram("dauphin")
print(g.pages["accueil"])

cost = grid_cost(g,corpus,None,0)

print(cost)
