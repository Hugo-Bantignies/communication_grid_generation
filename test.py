from PictogramGrid import Pictogram,Page,Grid
from EvaluationGrid import sentence_distance_cost
import os
import time

corpus = []

for root, dirs, files in os.walk("./tcof_dataset/transcripts"):
    for name in files:
        corpus.append(os.path.join(root,name))

g = Grid(corpus,randomizer=False,warnings = False)

start_time = time.time()
cost = 0
eval_size = 10000

for i in range(eval_size):
    s = "puzzle refaire peur école vrai abeille petit chat chien arbre".split(" ")
    cost += sentence_distance_cost(g,s)

print("-- %s seconds --" % (time.time() - start_time))
print("Number of sentences : ",eval_size)
print("Average size of sentence : ",len(s))
print("Cost : ",cost)
