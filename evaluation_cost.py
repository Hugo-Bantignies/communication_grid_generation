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

# FONCTIONS AUXILIAIRES POUR LE CALCUL DU COÛT DE PRODUCTION
#--------------------------------------------------------------

class WeightedPath:
    '''Classe auxiliaire pour stocker le chemin et le coût lors du calcul du chemin optimale'''

    def __init__(self):
        '''Constructeur'''

        self.path = []
        self.weight = 0


def initialNode(text, nodeList, edgeList, G, root_name):
    '''Fonction qui établit le noeud à partir duquel il faut commencer à calculer un arc

    :param text: texte d'entrée
    :type text: chaîne de charactères
    :param nodeList: liste de tous les noeuds du graphe
    :type nodeList: liste
    :param edgeList: tableau associatif de tous les arcs avec en clé le noeud tête et en valeurs le noeud pointé et le poids de l'arc
    :type edgeList: Dict
    :param G: graphe initial 
    :type G: classe: `networkx.DiGraph`
    :param root_name: name of the root page of the grid.
    :type root_name: string
    :return: liste avec le chemin et le poids total
    :rtype: liste
    '''

    path = []
    stock = []
    totalWeight = 0
    startNode = root_name

    # On parcours le fichier texte
    for line in text.splitlines():
        line = line.lower()
        line = line.strip()
        # On évite les lignes vides
        if line != "":
            # On récupère le plus court chemin
            words = shortestPath(startNode, line, nodeList, edgeList, G, root_name)
            path = words.path
            # On récupère le dernier élément de la liste
            startNode = path[-1]
            # On ajoute le poids
            totalWeight += words.weight

        finalPath = []
        # On ajoute le premier élément de la liste au chemin final
        finalPath.append(path[0])
        # On parcours le chemin
        for i in range(1, len(path)):
            # Si on toruve deux mots qui se suivent différents
            if path[i - 1] != path[i]:
                # on ajoute l'elt au chemin final
                finalPath.append(path[i])
        # On stocke dans une liste le chemin et le poids total
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
    '''Fonction de calcul du plus court path

    :param initialNode: point de départ de la recherche dans le graphe
    :type initialNode: Node
    :param sentance: phrase d'entrée pour laquelle il faut calculer le cout de production
    :type sentance: chaîne de charactères
    :param nodeList: liste de tous les noeuds du graphe
    :type nodeList: liste
    :param edgeList: tableau associatif de tous les arcs avec en clé le noeud tête et en valeurs le noeud pointé et le weight de l'arc
    :type edgeList: Dict
    :param G: graphe en question
    :type G: classe: networkx.DiGraph
    :param root_name: name of the root page of the grid.
    :type root_name: string
    :return: objet contenant le chemin final et le coût final
    :rtype: classe: `WeightedPath`
    '''

    initialNodes = []
    words = sentance.split(" ")
    shortestPath = []

    # Initialisation du poids total
    totalWeight = 0
    initialNodes.append(initialNode)
    
    # On créé la variable du chemin final
    finalPath = []
    pathList = []

    # On créé un nouveau graphe avec la liste des candidats
    coupleGraphe = nx.DiGraph()

    index = 0
    # On parcours la phrase
    for word in words:
        minWeight = 10000
        # On stocke dans une variable les mots "candidats" pour créer le plus court chemin        
        candidates = textToNodes(word, nodeList)

        # Pour chaque candidat
        for candidate in candidates:
            # On ajoute les candidats comme noeuds du sous graphe
            coupleGraphe.add_node(candidate)

            # Quand on arrive à l fin d ela phrase
            if index == len(words) - 1:
                # On créé un arc "end" de poids 0
                coupleGraphe.add_edge(candidate, "end", weight=0)
            elif index == 0:
                # On créé un arc "root_name" de poids 0
                coupleGraphe.add_edge(root_name, candidate, weight=0)

            # On parcours la liste des noeuds initiaux
            for firstNode in initialNodes:
                # On extrait le plus court chemin entre le premier noeud et le candidat avec la fonctionn "shortest_path "fonction Networkx
                try:
                    # graph = Digraph(filename='GGGG',format='png',comment='TEST_1')
                    path = nx.shortest_path(G, source=firstNode, target=candidate)
                except nx.NetworkXNoPath:                    
                    print ("No path between %s and %s." % (firstNode, candidate))
                
                # On initialise le poids
                weight = 0

                # On parcours le chemin
                for i in range(1, len(path)):
                    edgePrevNode = edgeList[path[i - 1]]
                    for edge in edgePrevNode:
                        # On vérifie que le premier elt de la variable arc = shortest path de i
                        if edge[0] == path[i]:
                            weight += edge[1]                                                        

                # Si le poids est inférieur au poids minimum
                if weight < minWeight:
                    # Le poids min prend la valeur du poids
                    minWeight = weight

                pathList.append(path)

                coupleGraphe.add_edge(path[0], path[-1], weight=weight)
                
        # On modifie le point de départ de la fonction
        initialNodes = candidates
        index = index + 1

        # On calcule la somme des poids entre les arcs
        totalWeight += minWeight
    
    # On applique à nouveau une recherche du plus court chemin dans le sous graphe
    try:        
        shortestpath = nx.shortest_path(coupleGraphe, source=root_name, target="end")
    except nx.NetworkXNoPath:

        print ("No path between %s and %s. Please check the input phrase" % (root_name, "end"))
        sys.exit()
        
    # On créé le chemin final
    wordIndex = 0

    # On parcours la liste des chemins
    for path in pathList:
        if (shortestpath[wordIndex] == path[0]) and (shortestpath[wordIndex + 1] == path[-1]):
            for words in path:
                finalPath.append(words)
            wordIndex = wordIndex + 1
    
    # On créé un objet
    weightedPath = WeightedPath()
    weightedPath.path = finalPath
    weightedPath.weight = totalWeight

    return weightedPath


def save_obj(obj, name ):
    '''Fonction qui stocke un objet dans un fichier .pkl

    :param obj: l'objet à stocker
    :type obj: any
    :param name: nom du fichier créé
    :type name: chaîne de charactères
    '''
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    '''Fonction qui récupere un objet contenu dans un fichier .pkl

    :param name: nom du fichier cible
    :type name: chaîne de charactères
    :return: renvoie le fichier avec nom `name`
    :rtype: any
    '''
    with open(name + '.pkl', 'rb') as f:

        return pickle.load(f)


def compute_cost(input_sentence, distances, root_name):
  '''Calcule le coût associé à la phrase d'entrée utilisant les distances données en entrée 

  :param input_sentence: phrase d'entrée
  :type input_sentence: chaîne de charactères
  :param distances: contient les distances entre chaque pictogramme 
  :type distances: chaîne de charactères
  :param root_name: name of the root page of the grid.
  :type root_name: string
  :return: le meilleur chemin et le coût final
  :rtype: liste
  '''
  # start_time = time.time()

  # variable qui garde le meilleur chemin et le coût final
  result = []
      
  # # On créé le graph G
  graph = nx.DiGraph()

  # tableau associatif (dict) qui comprendra les noeuds et les poids
  edgeList = {}

  # # On parcours les distances pour déterminer les noeuds, les arcs et les poids
  for line in distances.splitlines():
      line = line.strip()
      col = line.split('\t')
      
      # Addition du noeud au graphe
      graph.add_node(col[1])

      # Création des arcs avec leurs poids
      graph.add_edge(col[1], col[2], weight=col[3])

      # Création du tableau associatif 
      if col[1] in edgeList.keys():
          edgeList[col[1]].append((col[2], float(col[3])))
      else:
          edgeList[col[1]] = [(col[2], float(col[3]))]

  # création de la liste des noeuds
  nodeList = list(graph.nodes())

  output = initialNode(input_sentence, nodeList, edgeList, graph, root_name)

  # Sauvegarde des résultats
  for elt in output:
      result.append(elt)      

  # print("--- %s seconds ---" % '{:5.5}'.format(time.time() - start_time))

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
