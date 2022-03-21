from communication_grid import Grid
from evaluation_cost import *



g = Grid(["training_corpora/animal_proof_5.txt"],randomizer=False)

print("Cost : " + str(grid_cost(g,["training_corpora/animal_proof_5.txt"])))