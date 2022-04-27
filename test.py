from PictogramGrid import Pictogram,Page,Grid
from EvaluationGrid import grid_distance_cost
import os
import time

corpus = []

for root, dirs, files in os.walk("./tcof_dataset/transcripts"):
    for name in files:
        corpus.append(os.path.join(root,name))

g = Grid(corpus,randomizer=True,warnings = False)

g.display_information()

start_time = time.time()
cost = 0
eval_size = 30000

cost = grid_distance_cost(g,corpus)

print("-- %s seconds --" % (time.time() - start_time))
print("Cost : ",cost)
