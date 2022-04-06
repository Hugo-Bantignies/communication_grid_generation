from communication_grid import Grid
from evaluation_cost import *

g = Grid(["training_corpora/animals_corpus.txt"],randomizer=False)
g.display_information()
g.to_csv()

g.naive_cut(3,5)
g.to_csv()
g = Grid("default.csv")
g.display_information()
