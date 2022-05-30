from PictogramGrid import Pictogram,Page,Grid
from EvaluationGrid import grid_distance_cost,sentence_distance_cost,grid_cost
import os

g = Grid("test.csv")

g.display_information()

print(sentence_distance_cost(g,"hier".split(" ")))
