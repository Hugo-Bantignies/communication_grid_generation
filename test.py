from communication_grid import Grid
from evaluation_cost import *

g = Grid(["training_corpora/animals_corpus.txt"])
g.display_information()
g.naive_cut(3,3)
g.to_csv("test.csv")


g2 = Grid("test.csv")

for page in g2.pages.values():
    print(page.name)
    word_list = page.get_words()
    print(word_list)