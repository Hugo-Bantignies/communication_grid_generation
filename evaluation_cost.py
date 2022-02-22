#!python -m pip install networkx
#!python -m pip install matplotlib==2.2.3
#!python -m pip install ipywidgets
#!python -m pip install graphviz
#!python -m pip install pandas
#!python -m pip install pudb
#!python -m pip install nbconvert
#!python -m pip install nbconvert -U
#coding=utf-8


# %matplotlib
import matplotlib.pyplot as plt
import random
import copy
import math
import numpy as np
import sys
from graphviz import Digraph

# import time
import networkx as nx
from networkx import *
import pickle
# import pathlib
from argparse import ArgumentParser
from communication_grid import Grid

#=========================================================================================================================

def compute_distances(grid, movement_factor=1, selection_factor=1):
  '''Compute the distance between each pair of pictograms, within each page of the grid. 

  Takes in consideration the movement factor (difficulty of movement) and the selection factor (difficulty to select the pictogram)

  :param grid: grid to treat
  :type grid: classe: `Grid`
  :param movement_factor: movement factor, defaults to 1
  :type movement_factor: integer, (optional)
  :param selection_factor: selection factor, defaults to 1
  :type selection_factor: integer, (optional)
  :return: textual description of distances between each pair of pictogram.
  :rtype: string
  '''

  # Get the Core vocabulary of the grid (pictograms)
  disTab = grid.get_core_voc()
  # Copy of the dictionnary to use in the main loop
  distTab_copy = copy.deepcopy(disTab) 
  # Final distances
  distances = ''

  # Definition of the Movement factor
  m = movement_factor
  # Definition of Selection factor
  n = selection_factor

  for key1,picto1 in disTab.items():
    # Reference ID
    refID = key1
    # Name of the current page
    currentPage = picto1[3]
    # Coordinates of the first pictogram
    x1 = picto1[1]
    y1 = picto1[2]
    # Remove the pictogram (to avoid redundant computation)
    distTab_copy.pop(key1)
    
    for key2,picto2 in distTab_copy.items():
      # Identifier of the second pictogram
      ID = key2

      # Checking if the page of the first pictogram is the same than the second one.
      currentPage2 = picto2[3]
      x2 = picto2[1]
      y2 = picto2[2]

      if currentPage2 == currentPage:
        # If the two pictograms are different.
        if refID != ID:
          # Euclidiant distance between the two pictograms
          squaredDistance = (x1 - x2) ** 2 + (y1 - y2) ** 2
          pictoDistance = math.sqrt(squaredDistance)

          #If the second pictogram is a directory pictogram : C=(P1,P2)m
          if "_r@" in ID :
            #Formula without the selection factor (n)
            distances += "Word to Directory" + "\t" + refID + "\t" + ID + "\t" + str(pictoDistance * m) + "\n"

          #If the two pictograms are words and not directory : C=(P1,P2)m+n            
          else :
            distances += "Word to Word" + "\t" + refID + "\t" + ID + "\t" + str(pictoDistance * m + n) + "\n"
            distances += "Word to Word" + "\t" + ID + "\t" + refID + "\t" + str(pictoDistance * m + n) + "\n"

    # Write the link between a directory pictogram (plus, return, pagination, return arrow et directories) and the page.
    if picto1[4]:
      # Formula of the selection action: C=n
      distances += "Directory pictogram to Page" + "\t" + refID + "\t" + picto1[4] + "\t" + str(n) + "\n"

    # Wtrit the link between the page and the directory pictogram 
    # Compute the distance between the link of the page and the pictograms from the top left pictogram (x=1 et y=1).
    squaredDistance3 = (1 - x1) ** 2 + (1 - y1) ** 2
    pageToPicto = math.sqrt(squaredDistance3)

    #If the second pictogram is a directory : C=(P(1,1)P2)m
    if "_r@" in picto1[0] :
      #Computation without the selection factor (n)
      distances += "Page to Directory pictogram" + "\t" + currentPage + "\t" + picto1[0] + "\t" + str(pageToPicto* m) + "\n"
    # If the second pictogram is a word : C=(P(1,1)P2)m+n
    else :
      distances += "Page to Word" + "\t" + currentPage + "\t" + refID + "\t" + str(pageToPicto * m + n) + "\n"

  return distances

#=========================================================================================================================

# AUXILIARY FUNCTIONS FOR THE COMPUTATION OF THE PRODUCTION COST
#--------------------------------------------------------------

class WeightedPath:
    '''Auxiliary class to store the path and the cost for the computation of the optimal path. pour stocker'''

    def __init__(self):
        '''Constructor'''

        self.path = []
        self.weight = 0


def initialNode(text, nodeList, edgeList, G, root_name):
    '''Function that initialize the node to start to compute an arc.

    :param text: input text
    :type text: string
    :param nodeList: list of all nodes of the graph
    :type nodeList: list
    :param edgeList: array of all arcs with for key : head node and value : pointed node and the weight of the arc.
    :type edgeList: Dict
    :param G: initial graph
    :type G: class: `networkx.DiGraph`
    :param root_name: name of the root page of the grid.
    :type root_name: string
    :return: list with the path and the total weight.
    :rtype: list
    '''

    path = []
    stock = []
    totalWeight = 0
    startNode = root_name

    # Explore the entire input file
    for line in text.splitlines():
        line = line.lower()
        line = line.strip()
        # Avoid empty lines
        if line != "":
            # Compute and get the shortest path
            words = shortestPath(startNode, line, nodeList, edgeList, G, root_name)
            path = words.path
            # Get the last element of the list
            startNode = path[-1]
            # Add the weight of the path
            totalWeight += words.weight

        finalPath = []
        # Add the first element of the list to the final path
        finalPath.append(path[0])
        # Explore the path
        for i in range(1, len(path)):
            # If two different consecutive words.
            if path[i - 1] != path[i]:
                # Add the element to the final path.
                finalPath.append(path[i])
        # Store in a list the final path and the total weight. 
        stock.append((finalPath, totalWeight))

    return stock


def textToNodes(word, nodeList):
    '''Fonction qui prend en entrée un mot de la phrase et en fait une liste de noeuds possibles

    :param word: chaque word de la phrase d'entrée
    :type word: chaîne de charactères
    :param nodeList: liste de tous les noeuds du graphe
    :type nodeList: liste
    :return: liste des noeuds canidats potentiels
    :rtype: liste
    '''
    candidatesNode = []
    # on parcours la liste des noeuds
    for i in range(0, len(nodeList)):
        # on découpe au '@' pour récupérer le mot d'origine au lieu de l'identifiant complet
        wordNode = nodeList[i].split("@")
        # Si le mot d'origine est égal au word de la phrase
        if wordNode[0] == word:
            # on l'ajoute à la liste des noeuds canidats potentiels
            candidatesNode.append(nodeList[i])

    return candidatesNode


def shortestPath(initialNode, sentance, nodeList, edgeList, G, root_name):
    '''Function to compute the shortest path

    :param initialNode: strarting point of the research
    :type initialNode: Node
    :param sentance: input sentence from which it will compute the cost
    :type sentance: string
    :param nodeList: list of all nodes of the graph
    :type nodeList: list
    :param edgeList: array of all arcs with for key : head node and value : pointed node and the weight of the arc.
    :type edgeList: Dict
    :param G: initial graph
    :type G: class: `networkx.DiGraph`
    :param root_name: name of the root page of the grid.
    :type root_name: string
    :return: object containing the final path and the final cost.
    :rtype: classe: `WeightedPath`
    '''

    initialNodes = []
    words = sentance.split(" ")
    shortestPath = []

    # Initialisation of the total weight
    totalWeight = 0
    initialNodes.append(initialNode)
    
    # Creation of the final path
    finalPath = []
    pathList = []

    # Creation of a sub graph containing the candidate list
    coupleGraphe = nx.DiGraph()

    index = 0
    # Exploration of the phrase
    for word in words:
        minWeight = 10000
        # Store the candidates words to compute the shortest path.      
        candidates = textToNodes(word, nodeList)

        # For each candidate
        for candidate in candidates:
            # Add the candidates as node of the sub graph
            coupleGraphe.add_node(candidate)

            # When we reach the end of the sentence
            if index == len(words) - 1:
                # Cration of the "end" arc with a weight of 0
                coupleGraphe.add_edge(candidate, "end", weight=0)
            elif index == 0:
                # Creation of the "root_name" arc with a weight of 0
                coupleGraphe.add_edge(root_name, candidate, weight=0)

            # Exploration of the list of initial nodes.
            for firstNode in initialNodes:
                # Extraction of the shortest path between the first node and the candidate with the "shortest_path" function of Networkx.
                try:
                    path = nx.shortest_path(G, source=firstNode, target=candidate)
                except nx.NetworkXNoPath:                    
                    print ("No path between %s and %s." % (firstNode, candidate))
                
                # Initialization of the weights
                weight = 0

                # Exploration of the path
                for i in range(1, len(path)):
                    edgePrevNode = edgeList[path[i - 1]]
                    for edge in edgePrevNode:
                        # Check if the first element and the arc correspond to the shortest path.
                        if edge[0] == path[i]:
                            weight += edge[1]                                                        

                # If the weight is lower than the minimum weight.
                if weight < minWeight:
                    # The minimum weight becomes the weight.
                    minWeight = weight

                pathList.append(path)

                coupleGraphe.add_edge(path[0], path[-1], weight=weight)
                
        # New starting point
        initialNodes = candidates
        index = index + 1

        # Computation of the sum of all weights.
        totalWeight += minWeight
    
    # New computaton of the shortest path in the sub graph.
    try:        
        shortestpath = nx.shortest_path(coupleGraphe, source=root_name, target="end")
    except nx.NetworkXNoPath:

        print ("No path between %s and %s. Please check the input phrase" % (root_name, "end"))
        sys.exit()
        
    # Final path
    wordIndex = 0

    # Exploration of all paths
    for path in pathList:
        if (shortestpath[wordIndex] == path[0]) and (shortestpath[wordIndex + 1] == path[-1]):
            for words in path:
                finalPath.append(words)
            wordIndex = wordIndex + 1
    
    # Creation of the object
    weightedPath = WeightedPath()
    weightedPath.path = finalPath
    weightedPath.weight = totalWeight

    return weightedPath


def save_obj(obj, name ):
    '''Function to store an object in a .pkl file.

    :param obj: object to store
    :type obj: any
    :param name: name of the file
    :type name: string
    '''
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    '''Function to get an object in a .pkl file. 

    :param name: name of the target file.
    :type name: string
    :return: return the file with the name : `name`
    :rtype: any
    '''
    with open(name + '.pkl', 'rb') as f:

        return pickle.load(f)


def compute_cost(input_sentence, distances, root_name):
  '''Compute the associated cost of the input sentence and the computed distances (arcs)

  :param input_sentence: source sentence
  :type input_sentence: string
  :param distances: distance between each pictograms (arcs)
  :type distances: string
  :param root_name: name of the root page of the grid.
  :type root_name: string
  :return: best path and the final cost
  :rtype: list
  '''
  # start_time = time.time()

  # Best path and final cost
  result = []
      
  # # Creation of the graph g
  graph = nx.DiGraph()

  # Dictionary contaning the nodes and the weights (edges)
  edgeList = {}

  # # Exploration of the distances to determine the nodes, the arcs and the weights.
  for line in distances.splitlines():
      line = line.strip()
      col = line.split('\t')
      
      # Add the node to the graph
      graph.add_node(col[1])

      # Arc creation with its weight
      graph.add_edge(col[1], col[2], weight=col[3])

      # Creation of the edge dictionary. 
      if col[1] in edgeList.keys():
          edgeList[col[1]].append((col[2], float(col[3])))
      else:
          edgeList[col[1]] = [(col[2], float(col[3]))]

  # Creation of the list of nodes.
  nodeList = list(graph.nodes())

  output = initialNode(input_sentence, nodeList, edgeList, graph, root_name)

  # Save results
  for elt in output:
      result.append(elt)      

  return result


def grid_cost(grid,input_file,root_name = "accueil"):

    '''Main function to compute the cost of a given grid and a source file.

    :param grid: Input grid to evalute its cost.
    :type grid: class: Grid
    :param input_file: source file containing sentences for the evaluation.
    :type input_file: file (`.txt`)
    :return: cost of the grid for the input file. 
    :rtype: float
    '''
    #Arcs and distance generation for the given grid
    arcs = compute_distances(grid)
    
    #The source file is a '.txt' file
    if(input_file.endswith('.txt')):

      #Source file opening
      with open(input_file,"r") as rawFile:

        cost = 0
        #For each line in the file, split the line
        for line in rawFile:
            line = line.strip()
            #Cost computation
            result = compute_cost(line,arcs,root_name)
            cost+=result[0][1]

        return cost
    
    #The source file is not a '.txt' file
    else:
      raise Exception("Incorrect file format !")
