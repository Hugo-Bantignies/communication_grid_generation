#Imports

import sys
sys.path.insert(1, './..')
from PictogramGrid import Grid
from EvaluationGridBis import grid_distance_cost,grid_similarity_cost
import math

def grids_evaluation(ga_path, gb_path, corpus):
    #Loading the PODD and the optimized grid (from TCOF dataset)
    ga = Grid(ga_path,synonyms_file = "podd_syn.json")
    gb = Grid(gb_path)

    nb_page_a = len(ga.pages)
    nb_page_b = len(gb.pages)

    ga_infos = [ga.nb_picto,len(ga.pages)]
    gb_infos = [gb.nb_picto,len(gb.pages)]

    print(ga_path.strip(".csv"),": - Number of pictos :",ga_infos[0],"   Number of pages : ",ga_infos[1])
    print(gb_path.strip(".csv"),": - Number of pictos :",gb_infos[0],"   Number of pages : ",gb_infos[1])


    sim_coef = 0.5

    #Common miss_list computation
    _,ga_mm,ga_miss_list,_ = grid_distance_cost(ga,corpus,synonyms_file = "podd_syn.json",missmatch_mode = True)
    _,gb_mm,gb_miss_list,_ = grid_distance_cost(gb,corpus,synonyms_file = None,missmatch_mode = True)

    common_miss_list = ga_miss_list.union(gb_miss_list)

    print("MISMATCHES (A) : ",ga_mm,"     MISSING WORDS (A) :",len(ga_miss_list))
    print("MISMATCHES (B) : ",gb_mm,"     MISSING WORDS (B) :",len(gb_miss_list))
    print("COMMON MISSING WORDS : ",len(common_miss_list))

    #Cost computation
    ga_dist,ga_mm,miss_list,ga_stats = grid_distance_cost(ga,corpus,synonyms_file = "podd_syn.json",missmatch_mode = False,stopwords = common_miss_list)
    ga_cohe = grid_similarity_cost(ga,sim_matrix = "podd_sim.json",synonyms_file = "podd_syn.json",missmatch_mode = False)
    ga_cost = (math.log10(ga_cohe/nb_page_a) * sim_coef) +  (math.log10(ga_dist) * (1 - sim_coef))

    print("SIMILARITY COEFFICIENT :",sim_coef)

    #Print PODD results
    print("====="+str(ga_path.strip(".csv"))+"=====")
    print("Mismatches :",ga_mm,"      Missing words :",len(miss_list))
    print("Dist(G) :",math.log(ga_dist))
    print("Cohe(G) :",math.log(ga_cohe/nb_page_a))
    print("Cost(G) :",ga_cost)

    gb_dist,gb_mm,gb_miss_list,_ = grid_distance_cost(gb,corpus,synonyms_file = None,missmatch_mode = False,stopwords = common_miss_list)
    gb_cohe = grid_similarity_cost(gb,sim_matrix = "../sim_matrices/tcof_sim.json",missmatch_mode = False)
    gb_cost = (math.log10(gb_cohe/nb_page_b) * sim_coef) +  (math.log10(gb_dist) * (1 - sim_coef))


    #Print TCOF results
    print("====="+str(gb_path.strip(".csv"))+"=====")
    print("Mismatches :",gb_mm,"      Missing words :",len(gb_miss_list))
    print("Dist(G) :",math.log(gb_dist),"   ("+str(((1 - (gb_dist/ga_dist))*100) * - 1)+"%)")
    print("Cohe(G) :",math.log(gb_cohe/nb_page_b))
    print("Cost(G) :",gb_cost)