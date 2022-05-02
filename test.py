from PictogramGrid import Pictogram,Page,Grid
from EvaluationGrid import grid_distance_cost,sentence_distance_cost
from gpgo import gpgo
import os

corpus = ["training_corpora/animals_corpus.txt"]

for root, dirs, files in os.walk("training_corpora"):
    for name in files:
        pass#corpus.append(os.path.join(root,name))

'''my_gpgo= gpgo(corpus,corpus,pop_size=200,cross_proba=0.5,cross_info_rate=0.5,mutation_proba=0.5,select_number=50,gen_number=500,randomizer=True)
my_gpgo.display_config()

g = my_gpgo.genetic_algorithm()

print(g.pages["accueil"])
g.to_csv()'''

'''g = Grid(corpus,randomizer=False,warnings = False)
g.to_csv()

for p in g.pages.values():
    print(p.name)
    print(p)
cost = sentence_distance_cost(g,"chat dauphin".split(" "))

print("Cost : ",cost)'''

g = Grid(corpus,randomizer=False,warnings = False)
picto_a = g.pages["accueil"].pictograms["dauphin"]
picto_b = g.pages["default0"].pictograms["singe"]

g.swap_pictograms(picto_a,picto_b)

picto_a = g.pages["default0"].pictograms["dauphin"]
picto_b = g.pages["default1"].pictograms["feuilles"]

g.swap_pictograms(picto_a,picto_b)

for p in g.pages.values():
    print(p)