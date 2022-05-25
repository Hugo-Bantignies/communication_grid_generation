from cProfile import label
from PictogramGrid import Pictogram,Page,Grid
from EvaluationGrid import grid_distance_cost,sentence_distance_cost,grid_cost
import matplotlib.pyplot as plt
from gpgo import gpgo,load_gpgo
from mp_gpgo import mp_gpgo
import os

if(__name__ == "__main__"):

    corpus = []
    input_csv_file = "default.csv"

    for root, dirs, files in os.walk("training_corpora"):
        for name in files:
            corpus.append(os.path.join(root,name))

    configs = ["config/default.yaml","config/test1.yaml","config/test2.yaml","config/test3.yaml"]

    my_gpgo = mp_gpgo(corpus,corpus,configs,nb_proc = 4)
    g = my_gpgo.mp_genetic_algorithm()

    g.display_information()

    hist = my_gpgo.mp_fitness_history()

    i = 0
    for h in hist:

        plt.plot(h,label="p"+str(i))
        i = i + 1

    plt.legend()
    plt.show()

    
