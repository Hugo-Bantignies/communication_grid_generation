import math
import codecs
from PictogramGrid import Grid
from PageTree import *

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
        
        for i in range(best_distance):
            #If go up, just add the selection of the return (not a pictogram, constant)
            if(best_path[i].parent == best_path[i+1]):
                pass
            
            #If go down, find the pictogram of the associated next page and compute distance
            elif(best_path[i+1] in best_path[i].children):
                child_name = best_path[i+1].page
                picto_row = grid.pages[best_path[i].page].pictograms[child_name].row
                picto_col = grid.pages[best_path[i].page].pictograms[child_name].col
                movement_dist += euclidean_dist(0,0,picto_row,picto_col)

        #Final distance to compute in the final page
        if(best_distance == 0):
            picto_b = grid.pages[best_path[1].page].pictograms[end_word]
            if(start_word == "--start"):
                movement_dist += euclidean_dist(0,0,picto_b.row,picto_b.col)
            else:
                picto_a = grid.pages[best_path[0].page].pictograms[start_word]
                movement_dist += euclidean_dist(picto_a.row,picto_a.col,picto_b.row,picto_b.col)

        #Final cost computation
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