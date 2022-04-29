from audioop import cross
from PictogramGrid import Pictogram,Page,Grid
from EvaluationGrid import grid_distance_cost,sentence_distance_cost
from gpgo import gpgo
import os
import time

corpus = ["training_corpora/animal_proof_5.txt"]

for root, dirs, files in os.walk("training_corpora"):
    for name in files:
        pass#corpus.append(os.path.join(root,name))

my_gpgo= gpgo(corpus,corpus,pop_size=100,cross_proba=0.5,cross_info_rate=0.5,mutation_proba=0.5,select_number=50,gen_number=500,randomizer=True)
my_gpgo.display_config()

g = my_gpgo.genetic_algorithm()

g.to_csv()

'''g = Grid(corpus,randomizer=False,warnings = False)
g.to_csv()

for p in g.pages.values():
    print(p.name)
    print(p)
cost = sentence_distance_cost(g,"le chat".split(" "))

print("Cost : ",cost)'''

