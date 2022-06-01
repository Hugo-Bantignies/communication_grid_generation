import math
import codecs
import json
from PictogramGrid import Grid,Page,Pictogram
from PageTree import *
from tqdm import tqdm


#===================================================================
# MATHS FUNCTIONS
#===================================================================

def euclidean_dist(x1,y1,x2,y2):
    '''Function that computes the Euclidean distance between two elements
    :param x1: x position of the first element
    :type: integer
    :param y1: y position of the first element
    :type: integer
    :param x2: x position of the second element
    :type: integer
    :param y2: y position of the second element
    :type: integer
    :return: Euclidean distance between element 1 and element 2
    :rtype: float
    '''

    return math.sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))


def manhattan_dist(x1,y1,x2,y2):
    '''Function that computes the Manhattan distance between two elements
    :param x1: x position of the first element
    :type: integer
    :param y1: y position of the first element
    :type: integer
    :param x2: x position of the second element
    :type: integer
    :param y2: y position of the second element
    :type: integer
    :return: Manhattan distance between element 1 and element 2
    :rtype: intger
    '''
    return abs((x1 - x2)) + abs((y1 - y2))

def dot_product(v_a,v_b):
    '''Function to compute the dot product between two vectors'''
    
    dot_product = 0

    for i in range(len(v_a)):   
        dot_product = dot_product + v_a[i] * v_b[i]
    
    return dot_product

def magnitude(v_a):
    '''Function to compute the magnitude/norm of a vector'''

    vector_sum = 0

    for i in range(len(v_a)):
        vector_sum = vector_sum + v_a[i] * v_a[i]
    
    return math.sqrt(vector_sum)


def cosine_similarity(v_a,v_b):
    '''Function to compute the cosine_similarity of two vectors'''
    if(magnitude(v_a) * magnitude(v_b) != 0):
        return dot_product(v_a,v_b) / (magnitude(v_a) * magnitude(v_b))
    else:
        return 0


#===================================================================
# COST COMPUTATION
#===================================================================

def sentence_distance_cost(grid,sentence,movement_coef = 1,selection_coef = 1,synonyms_refs = None, missmatch_mode = False):

    #Computation of the euler tour (just one time is needed)
    if(grid.page_tree.eulerian_values == None):
        grid.page_tree.eulerian_values = euler_tour(grid.page_tree,0)

    #Beginning of the sentence
    start_word = "--start"
    cost = 0
    missmatches = 0
    miss_list = []

    for word in sentence:
        #Next word
        end_word = word

        #If synonym pictograms
        if(synonyms_refs != None):
            if(word in synonyms_refs):
                end_word = synonyms_refs[word]

        #print("DEBUG : Words :",start_word,end_word)

        #Potential pages (contain the word)
        potential_pages = []

        #--------------------------------------------------------
        #PATH FINDING BETWEEN THE STARTING WORD AND THE NEXT WORD
        #--------------------------------------------------------

        missmatch = False

        #If missmatches are allowed
        if(missmatch_mode == True):
            if(end_word not in grid.picto_voc):
                missmatches += 1
                missmatch = True
                if(end_word not in miss_list):
                    miss_list.append(end_word)
        
        if(missmatch == False):
            #Find pages containing the word
            potential_pages = grid.picto_voc[end_word]

            #The node is the root at the beginning
            if(start_word == "--start"):
                start_node = grid.page_tree
            
            best_distance = math.inf
            page_pict_dist = math.inf
            best_path = []

            #For each potential page, computation of the path to keep the smallest
            for page in potential_pages:
                end_node = page

                #Computation of the distance at the end
                end_picto = grid.pages[end_node.page].pictograms[end_word]
                new_page_pict_dist = euclidean_dist(0,0,end_picto.row,end_picto.col)

                #Computation of the path in the tree
                result = path_finding(grid.page_tree,start_node,end_node)

                #Keeping the best path
                if(result[0] + new_page_pict_dist < best_distance + page_pict_dist):
                    best_distance = result[0]
                    best_path = result[1]

            #-----------------------------------------------------------------
            #COMPUTATION OF THE DISTANCE BETWEEN PICTOGRAMS FOLLOWING THE PATH
            #-----------------------------------------------------------------

            movement_dist = 0
            selection_dist = best_distance + 1

            #Get the starting pictogram
            if(start_word == "--start"):
                picto_start = Pictogram("--start",0,0,grid.root_name,None,None)
            else:
                picto_start = grid.pages[best_path[0].page].pictograms[start_word]

            #print("DEBUG : Best distance : ",best_distance)

            for i in range(len(best_path)):

                #End of the path
                if(i == best_distance):
                    next_picto = grid.pages[best_path[i].page].pictograms[end_word]
                    #print("DEBUG : End page",picto_start,"-->",next_picto)
                    break
                
                #Navigation in the tree
                else:
                    #Up
                    if(best_path[i].parent == best_path[i+1]):
                        next_picto = Pictogram("--start",0,0,best_path[i+1].page,None,None)
                        #print("DEBUG : UP",picto_start,"-->",next_picto)
                        movement_dist += euclidean_dist(picto_start.row,picto_start.col,next_picto.row,next_picto.col)
                        picto_start = next_picto

                    #Down   
                    else:
                        next_picto = grid.pages[best_path[i].page].pictograms[best_path[i+1].page]
                        #print("DEBUG : DOWN",picto_start,"-->",next_picto)
                        movement_dist += euclidean_dist(picto_start.row,picto_start.col,next_picto.row,next_picto.col)
                        picto_start = Pictogram("--start",0,0,best_path[i+1].page,None,None)

            movement_dist += euclidean_dist(picto_start.row,picto_start.col,next_picto.row,next_picto.col)

            cost += movement_dist * movement_coef + selection_dist * selection_coef

            #The end becomes the start for the previous iteration
            start_word = end_word
            start_node = end_node

    return cost,missmatches,miss_list

def grid_distance_cost(grid,input_corpus,synonyms_file = None,missmatch_mode = False):

    '''Main function to compute the cost of a given grid and a source file.

    :param grid: Input grid to evalute its cost.
    :type grid: class: Grid
    :param input_file: source file containing sentences for the evaluation.
    :type input_file: file (`.txt`)
    :return: cost of the grid for the input file. 
    :rtype: float
    '''
    
    cost = 0
    missmatches = 0
    missmatch_list = []
    n = 0

    synonyms_refs = None

    if(synonyms_file != None and synonyms_file.endswith(".json")):
        #File opening
        file = codecs.open(synonyms_file,"r","utf-8")

        #Load the similarity matrix
        synonyms_refs = json.load(file)
    
    for file_path in input_corpus:

        #The source file is a '.txt' file
        if(file_path.endswith('.txt')):

            #Source file opening
            with codecs.open(file_path,"r","utf-8") as rawFile:

                #For each line in the file, split the line
                for line in rawFile:
                    #Line preparation
                    line = line.strip()
                    line = line.split(" ")
                    #Cost computation
                    results = sentence_distance_cost(grid,line,synonyms_refs = synonyms_refs,missmatch_mode=missmatch_mode)
                    cost+=results[0]
                    missmatches+=results[1]
                    missmatch_list = missmatch_list + results[2]
                    n = n + 1
                    
        #The source file is not a '.txt' file
        else:
            raise Exception("Incorrect file format !")
            
    #Return the cost
    return cost,missmatches,set(missmatch_list)

def compute_word_similarities(voc,model):
    '''Function to compute the similarities between all words and returns a dictionary'''
    sim_matrix = dict()

    for i in tqdm(range(len(voc)),desc = "Similarities computation ",unit = "word"):
        
        wi = voc[i]
        wi_sims = dict()

        #Get the vector of the word wi
        vec_wi = model.get_word_vector(wi)

        for wj in voc:

            #Compute the similarity between the two words
            word_score = 1 - cosine_similarity(vec_wi,model.get_word_vector(wj))
            #Store it
            wi_sims.update({wj : word_score})

        #Store all similarities with the word wi
        sim_matrix.update({wi : wi_sims})

    return sim_matrix

def page_similarity_cost(page,sim_matrix):
    '''Function to return the similarity cost of a page'''

    #Initialization
    cost = 0
    words = page.get_words()

    for wi in words:
        #Score for a word
        word_score = 0

        for wj in words:
            #Compute the similarity between the two words
            word_score += sim_matrix[wi][wj]

        #Update the similarity score of the pictogram
        page.pictograms[wi].similarity_score = 1 - (word_score / page.nb_picto)

        cost = cost + word_score
    
    return cost

def grid_similarity_cost(grid,sim_matrix):
    '''Function to compute the similarity cost of an entire grid'''

    cost = 0

    #Compute the similarity of each page
    for page in grid.pages.values():
        
        cost += page_similarity_cost(page,sim_matrix)

    return cost

def grid_cost(grid,input_corpus,sim_matrix,similarity_coefficient = 0.5,synonyms_file = None, missmatch_mode = False):
    '''Function to evaluate a grid depending on the similarity coefficient'''

    #If the cost is only depending on the distance
    if(similarity_coefficient == 0):
        dist,mms,_ =  grid_distance_cost(grid,input_corpus,synonyms_file,missmatch_mode)
        return math.log10(dist)

    #If the cost is only depending on the similarity
    elif(similarity_coefficient == 1):
        sim =  grid_similarity_cost(grid,sim_matrix)
        return math.log10(sim)

    #Hybrid format
    else:
        dist = grid_distance_cost(grid,input_corpus)
        sim = grid_similarity_cost(grid,sim_matrix)

        return math.log10(sim) * similarity_coefficient + math.log10(dist) * (1 - similarity_coefficient)