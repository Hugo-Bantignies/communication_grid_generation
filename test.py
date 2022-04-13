from communication_grid import Grid
from evaluation_cost import *

g = Grid(["training_corpora/animals_corpus.txt"])
g.display_information()
print(g.picto_voc)
g.naive_cut(3,3)
g.display_information()
print(g.picto_voc)
g.to_csv()