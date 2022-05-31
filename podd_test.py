from PictogramGrid import Pictogram,Page,Grid
from EvaluationGrid import grid_distance_cost,sentence_distance_cost,grid_cost
import os

podd = Grid("podd.csv")
tcof = Grid("default.csv")

print("PODD : ",sentence_distance_cost(podd,"oups maman aimer".split(" ")))
print("TCOF : ",sentence_distance_cost(tcof,"oups maman aimer".split(" ")))
