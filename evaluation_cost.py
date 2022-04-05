import math
import codecs

#Communication grid
from communication_grid import Grid


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

def sentence_cost(grid, sentence, distance_mode, movement_factor = 1, selection_factor = 1, root_name = "accueil"):
    '''Function to compute the cost of a grid (with only one main page)
    :param grid: grid from which the cost will be computed
    :type: class: Grid
    :param sentence: sentence use to compute the cost
    :type: list of string
    :param distance_mode: way of computing the distance (euclidean or manhattan)
    :type: string
    :movement_factor: returns
    :type: integer
    :return: returns the cost of the sentence for the grid
    :rtype: float or integer
    '''

    #Initialization
    grid_voc = grid.picto_voc
    cost = 0
    pic_s = None
    pic_e = None

    picto_list = []

    #For each word in the sentence
    for word in sentence:
        
        #Access the dictionary to get the word (O(1) in average for a python dict)
        picto_list.append(grid_voc[str(word)+"@"+root_name])

    #For each word in the sentence
    for i in range(len(picto_list)):
        
        #Condition to not go beyond the limits
        if(i < len(picto_list) - 1):
            pic_s = picto_list[i]
            pic_e = picto_list[i + 1]

            if(pic_s and pic_e):

                #Euclidean distance
                if(distance_mode == "euclidean"):
                    cost = cost + selection_factor + euclidean_dist(pic_s[1],pic_s[2],pic_e[1],pic_e[2]) * movement_factor

                #Manhattan distance
                elif(distance_mode == "manhattan"):
                    cost = cost + selection_factor + manhattan_dist(pic_s[1],pic_s[2],pic_e[1],pic_e[2]) * movement_factor
    return cost



def grid_cost(grid,input_corpus,root_name = "accueil", average_option = True, distance_mode = "euclidean"):

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
                    result = sentence_cost(grid,line,distance_mode)
                    cost+=result
                    n = n + 1
                    
        #The source file is not a '.txt' file
        else:
            raise Exception("Incorrect file format !")

    #Return the average cost
    if(average_option):
        return (cost / n)
            
    #Return the cost
    else:
        return cost
