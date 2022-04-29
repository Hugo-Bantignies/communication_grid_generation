import math
import codecs
from PictogramGrid import Grid,Page,Pictogram
from PageTree import *


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

    return dot_product(v_a,v_b) / (magnitude(v_a) * magnitude(v_b))


#===================================================================
# COST COMPUTATION
#===================================================================

def sentence_distance_cost(grid,sentence,movement_coef = 1,selection_coef = 1):

    #Computation of the euler tour (just one time is needed)
    if(grid.page_tree.eulerian_values == None):
        grid.page_tree.eulerian_values = euler_tour(grid.page_tree,0)

    #Beginning of the sentence
    start_word = "--start"
    cost = 0

    for word in sentence:
        #Next word
        end_word = word

        #Potential pages (contain the word)
        potential_pages = []

        #--------------------------------------------------------
        #PATH FINDING BETWEEN THE STARTING WORD AND THE NEXT WORD
        #--------------------------------------------------------

        #Find pages containing the word
        potential_pages = grid.picto_voc[end_word]

        #The node is the root at the beginning
        if(start_word == "--start"):
            start_node = grid.page_tree
        
        best_distance = math.inf
        best_path = []

        #For each potential page, computation of the path to keep the smallest
        for page in potential_pages:
            end_node = page

            result = path_finding(grid.page_tree,start_node,end_node)
            if(result[0] < best_distance):
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
                    movement_dist += manhattan_dist(picto_start.row,picto_start.col,next_picto.row,next_picto.col)
                    picto_start = next_picto

                #Down   
                else:
                    next_picto = grid.pages[best_path[i].page].pictograms[best_path[i+1].page]
                    #print("DEBUG : DOWN",picto_start,"-->",next_picto)
                    movement_dist += manhattan_dist(picto_start.row,picto_start.col,next_picto.row,next_picto.col)
                    picto_start = Pictogram("--start",0,0,best_path[i+1].page,None,None)

        movement_dist += manhattan_dist(picto_start.row,picto_start.col,next_picto.row,next_picto.col)

        cost += movement_dist * movement_coef + selection_dist * selection_coef

        #The end becomes the start for the previous iteration
        start_word = end_word
        start_node = end_node

    return cost

def grid_distance_cost(grid,input_corpus):

    '''Main function to compute the cost of a given grid and a source file.

    :param grid: Input grid to evalute its cost.
    :type grid: class: Grid
    :param input_file: source file containing sentences for the evaluation.
    :type input_file: file (`.txt`)
    :return: cost of the grid for the input file. 
    :rtype: float
    '''
    
    cost = 0
    n = 0
    
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
                    result = sentence_distance_cost(grid,line)
                    cost+=result
                    n = n + 1
                    
        #The source file is not a '.txt' file
        else:
            raise Exception("Incorrect file format !")
            
    #Return the cost
    else:
        return cost


def page_similarity_cost(page,model):
    '''Function to return the similarity cost of a page'''

    #Initialization
    cost = 0
    words = page.get_words()

    for wi in words:
        #Score for a word
        word_score = 0
        vec_wi = model.get_word_vector(wi)

        for wj in words:
            #Compute the similarity between the two words
            word_score += cosine_similarity(vec_wi,model.get_word_vector(wj))
        
        cost = cost + word_score
    
    return cost


def grid_similarity_cost(grid,model):
    '''Function to compute the similarity cost of an entire grid'''

    cost = 0

    #Compute the similarity of each page
    for page in grid.pages.values():
        
        cost += page_similarity_cost(page,model)

    return cost

def grid_cost(grid,input_corpus,model,similarity_coefficient):
    '''Function to evaluate a grid depending on the similarity coefficient'''

    #If the cost is only depending on the distance
    if(similarity_coefficient == 0):
        return grid_distance_cost(grid,input_corpus)

    #If the cost is only depending on the similarity
    elif(similarity_coefficient == 1):
        return grid_similarity_cost(grid,model)

    #Hybrid format
    else:
        dist = grid_distance_cost(grid,input_corpus)
        sim = grid_similarity_cost(grid,model)

        return (similarity_coefficient * sim) * ((1 - similarity_coefficient) * dist)
    
