from audioop import cross
from PictogramGrid import Pictogram,Page,Grid
from EvaluationGrid import grid_distance_cost
from gpgo import gpgo
import os
import time

corpus = []

for root, dirs, files in os.walk("training_corpora"):
    for name in files:
        corpus.append(os.path.join(root,name))

my_gpgo= gpgo(corpus,corpus,pop_size=100,cross_proba=0.5,cross_info_rate=0.5,mutation_proba=0.5,select_number=50,gen_number=20,randomizer=True)
my_gpgo.display_config()

g = my_gpgo.genetic_algorithm()

g.to_csv()
'''
g = Grid(corpus,randomizer=True,warnings = False)

start_time = time.time()
cost = 0
eval_size = 30000

cost = grid_distance_cost(g,corpus)

print("-- %s seconds --" % (time.time() - start_time))
print("Cost : ",cost)'''
