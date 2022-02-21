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
from argparse import ArgumentParser
# import pathlib

# ALGORITHME GÉNÉTIQUE
from deap import base
from deap import creator
from deap import tools


class Slot():
    '''Représente l'element le plus basique d'une grille.
    
    Il peut contenir un pictogramme ou être vide (None).

    :word: mot lié au pictpgramme
    :type word: chaîne de caractères
    :is_core: boolean qui indique si le mot associé fait partie du vocabulaire de base.
    :type is_core: boolean
    :page_destination: Eventuelle page de destination liée au pictogramme. Peut être nulle.
    :type page_destination: class: `Page`
    '''

    def __init__(self, word, is_core, page_destination):        
        '''Constructeur        
        '''        

        self.__word = copy.copy(word)
        self.__is_core = copy.copy(is_core)
        self.__page_destination = copy.copy(page_destination)

    def get_word(self):
        '''Accesseur
        
        :return: Renvoi le mot lié au slot
        :rtype: châine de charactères        
        '''

        return self.__word

    def get_is_core(self):
        '''Accesseur

        :return: Renvoi le boolean `is_core` du slot
        :rtype: boolean        
        '''

        return self.__is_core

    def get_page_destination(self):
        '''Accesseur
        
        :return: Renvoi la page de destination du slot
        :rtype: class: `Page`        
        '''

        return self.__page_destination

    def set_word(self, word):
        '''Setter. Mettre en place le mot du slot
        
        :word: mot à metre en place
        :type word: chaîne de caractères        
        '''

        self.__word = word

    def set_page_destination(self, page):
        '''Setter. Mettre en place la page de destination du slot
        
        :page: page à mettre en place
        :type page: class: `Page`        
        '''

        self.__page_destination = page

    def __str__(self):
        '''Méthode de affichage du slot
        
        :return: Renvoi l'information du slot
        :rtype: chaîne de charactères
        '''

        dest = self.__page_destination
        if dest:
            dest = self.__page_destination.get_name()

        return f'{self.__word}({dest})'


class Page():
    '''Une page est un arrangement 2D de slots avec une taille fixe

    :param name: le nom de la page
    :type name: chaîne de caractères
    :param row_size: La hauteur de la table (nombre de lignes)
    :type row_size: entier
    :param col_size: La largueur de la table (nombre de colonnes)
    :type col_size: entier
    '''

    def __init__(self, name, row_size, col_size):
        '''Constructeur'''  

        self.__name = name
        self.__row_size = row_size
        self.__col_size = col_size
        self.__full = False
        self.__slots = []
        self.__fill()
        self.__last_R = 0
        self.__last_C = 0


    def __fill(self):
      '''Initialise chacun des slots à None'''

      self.__slots = []
      for i in range(0, self.__row_size) :
        self.__slots.append([None])
        for j in range(0, self.__col_size) :
          self.__slots[i].append(None)


    def set_slot(self, slot, num_row, num_col):
      '''Setter. Ajoute le Slot `slot` en position `num_row`, `num_col` dans la page

      :param slot: slot à mettre en place 
      :type slot: class `Slot`
      :param num_row: nombre de la ligne 
      :type num_row: entier
      :param num_col: nombre de la colonne
      :type num_col: entier
      :raises Exception: exception de dépassement des indices.
      :return: renvoie l'ancienne valeur du slot
      :rtype: class `Slot`
      '''

      if (num_row >= self.__row_size) or (num_col >= self.__col_size):
        print(f'row={num_row}, col={num_col}')
        print(f'row_size={self.__row_size}, col_size={self.__col_size}')
                
        raise Exception('Error: slot row or col out of bounds') 

      old_value = self.__slots[num_row][num_col]
      self.__slots[num_row][num_col] = slot

      return old_value


    def set_name(self, name):
      '''Setter. Mettre en place le nom de la page

      :param name: nom à mettre en place
      :type name: chaîne de charactères
      :return: renvoie le nom affecté
      :rtype: chaîne de charactères
      '''
      self.__name = name

      return name

    
    def get_name(self):
      '''Accesseur. 

      :return: renvoie le nom actuel de la page
      :rtype: chaîne de charactères
      '''

      return self.__name


    def get_row_size(self):
      '''Accesseur. 

      :return: renvoie la hauteur de la page
      :rtype: entier
      '''

      return self.__row_size


    def get_col_size(self):
      '''Accesseur. 

      :return: renvoie la longueur de la page
      :rtype: entier
      '''

      return self.__col_size


    def get_slot(self, num_row, num_col):
      '''Accesseur. 

      :return: renvoie le slot affecté à la position `(num_row, num_col)` 
      :rtype: class: `Slot`
      '''

      return self.__slots[num_row][num_col]


    def get_slot_list(self):
      '''Accesseur

      :return: renvoie la liste de slots de la page
      :rtype: Liste de Slots
      '''

      return self.__slots
    

    def get_pictograms(self):
      '''Obtiens les informations des pictogrammes dans la page

      Produit un tableau d'attributes contenant toutes les informations (nom, ligne, colonne, nom de page, page de destination) de chaque pictogramme de la page courante.

      :return: renvoie un tableau d'attributes 
      :rtype: Dict
      '''

      current_page_name = self.get_name()
      attributes = {}
      for row in range(0, self.__row_size):
        for col in range (0, self.__col_size):
          slot = self.__slots[row][col]
          if slot:
            word = slot.get_word()
            dest = slot.get_page_destination()
            if dest:
              dest_page_name = dest.get_name()
            else:
              dest_page_name = None

            id = f'{word}@{current_page_name}'
            while id in attributes:
              id = f'{id}*'

            attributes[id] = [word, row, col, current_page_name, dest_page_name]  

      return attributes


    def is_free(self, num_row, num_col):
      '''Retourne vrai si le slot à la position (`num_row`, `num_col`) est libre, faux sinon.

      :param num_row: nombre de la ligne
      :type num_row: entier
      :param num_col: nombre de la colonne
      :type num_col: entier
      :return: renvoie un bolean
      :rtype: bolean
      '''
      return self.__slots[num_row][num_col] == None


    def is_full(self):
      '''Retourne vrai si la table est pleine (aucun slot vide), faux sinon

      :return: renvoie un bolean 
      :rtype: bolean
      '''

      if (self.__full):
        return True
      for row in range(0, self.__row_size):
        for col in range (0, self.__col_size):
          if self.__slots[row][col] == None:
            return False
      self.__full = True
      return True


    def add_word(self, word, core=False, dest=None) :
      '''Crée et ajoute un slot(pictogramme) dans le prochain emplacement disponible de la page 
      
      Fonction récursive.

      :param word: nom du mot du pictogramme
      :type word: chaîne de charactères
      :param core: indique si le mot est du voc de base, defaults to False
      :type core: boolean, optional
      :param dest: page de destination du pictogramme, defaults to None
      :type dest: classe: `Page`, optional
      :return: renvoie le nom du mot si affectation possible, null sinon 
      :rtype: chaîne de charactères
      '''

      if(self.__last_C == self.__col_size) : 
        self.__last_C = 0
        self.__last_R += 1

      if(self.__last_R == self.__row_size) :
        self.__full = True
        print("Failed to add word <", word, ">. The table is full.")

        return None

      if(self.__slots[self.__last_R][self.__last_C] == None) :
        s = Slot(word, core, dest)
        self.__slots[self.__last_R][self.__last_C] = s
        self.__last_R
        self.__last_C += 1

        return word
      
      self.__last_R
      self.__last_C += 1

      return self.add_word(word, dest=dest)

    #  (à revoir ? Efficacité chaînes de caractères)
    def __str__(self):
      '''Méthode d'affichage d'une page

      :return: renvoie la structure de la page dans un format lisible
      :rtype: chaîne de charactères
      '''

      s = "Page: " + self.__name + "\n("
      for i in range(0, self.__row_size) : 
        for j in range(0, self.__col_size) :
          s+=str(self.__slots[i][j])
          s+=", "
        s+='\n'

      return s+')'

    
class Grid():
  '''Meta-classe représentant la structure complète d'un système de grilles de pictogrammes 

  :param input_file: fichier `.csv` en format `Augcom` ou tableau d'attributes décrivant chaque pictogramme avec le format: {`id_picto` : [`nom`, `ligne`, `colonne`, `page`, `destination`]}
  :type input_file: fichier / Dict
  :param row_size: hauteur fixe de chaque page de la grille
  :type row_size: entier
  :param col_size: longueur fixe de chaque page de la grille
  :type col_size: entier
  :raises Exception: exception d'entrée incompatible  
  '''

  def __init__(self, input_file, row_size, col_size):
    '''Constructeur'''

    self.__row_size = row_size
    self.__col_size = col_size
    self.__core_voc = {}
    self.__pages = {}
    self.__pageCounter = 0     
    self.__fusion_id = 0
    self.__generate_random_grid(input_file)


  def get_root_page(self):
    '''Obtient la page racine, qui est par défaut la page nommé `accueil`

    :return: renvoi la page d'accueil 
    :rtype: classe: `Page`
    '''

    return self.__pages.get('accueil')

  
  def get_nb_pages(self):
    '''Renvoie le nombre de pages contenues dans la grille

    :return: nombre total de pages
    :rtype: entier
    '''

    return self.__pageCounter
  

  def get_page_names(self):
    '''Renvoie la liste de noms de pages contenues dans la grille

    :return: liste de noms
    :rtype: Liste
    '''

    return self.__pages.keys()


  def get_page(self, name):
    '''Renvoie la page avec le nom `name` 

    :param name: nom de la page à chercher
    :type name: chaîne de charactères
    :return: la page concernée
    :rtype: classe: `Page`
    '''

    return self.__pages.get(name) 


  def get_page_dict(self):
    '''Renvoie le tableau de pages de la grille

    :return: tableau de pages
    :rtype: Dict (format: {`page_name`: chaine de charactères : `page`: classe `Page`})
    '''

    return self.__pages


  def get_core_voc(self):
    '''Renvoie le tableau d'attributes décrivant tous les pictogrammes

    :return: tableau d'attributes
    :rtype: Dict (format: {`id_picto`:[`nom`,`ligne`,`colonne`,`page`, `page_dest`]})
    '''

    return self.__core_voc


  def get_row_size(self):
    '''Renvoie la hauteur de la grille

    :return: nombre de lignes
    :rtype: entier
    '''

    return self.__row_size


  def get_col_size(self):
    '''Renvoie la longueur de la grille

    :return: nombre de colonnes
    :rtype: entier
    '''

    return self.__col_size

  
  def add_word_in_root(self, word, dest=None):
    '''Ajoute un nouveau pictogramme à la page d'accueil dans la première position disponible

    :param word: nom du pictogramme
    :type word: chaîne de charactères
    :param dest: page de destination du pictogramme, defaults to None
    :type dest: classe `Page`, optional
    '''

    accueil_page = self.__pages.get('accueil')
    if accueil_page.is_full() :

      print('accueil complète, désolé')
      return

    accueil_page.add_word(word, dest=dest)

    return


  def add_new_page(self, name):
    '''Fonction d'encapsulation 

    Ajoute une nouvelle page à la grille

    :param name: le nom de la nouvelle page
    :type name: chaîne de charactères
    :return: la page ajoutée
    :rtype: classe: `Page`
    '''

    return self.__add_page(name)


  def __add_page(self, name_page):
    '''Ajoute une nouvelle page à la grille

    :param name_page: le nom de la nouvelle page
    :type name_page: chaîne de charactères
    :return: la page ajoutée
    :rtype: classe: `Page`
    '''

    page = Page(name_page, self.__row_size, self.__col_size)    
    self.__pages[name_page] = page
    self.__pageCounter += 1 

    return page


    ''''''
  def update_leaf_picto(self, extra_page):
    '''Affecte la page `extra_page` à un pictogramme disponible

    Recherche le premier pictogramme qui n'a pas de page de destination et mettre en place `extra_page` 
    comme destination. 

    :param extra_page: la page à affecter
    :type extra_page: classe: `Page`
    :return: Renvoie la page contenant le pictogramme trouvé.
    :rtype: classe: `Page`
    '''    

    core_voc_dict = self.get_core_voc()

    # Valider que la première page de la grille soit l'accueil, sinon la remettre à la tête du tableau
    pages_dict = self.get_page_dict()
    first_page_name = list(pages_dict.keys())[0]
    if first_page_name != 'accueil':
      # 1. convertir le tableau d'attribs à une liste de tuples 
      tuples = list(pages_dict.items())
      # 2. trouver l'indice de l'accueil dans le tableau d'attribs
      counter = 0
      for page_name in pages_dict:
        if page_name == 'accueil':
          break
        counter+=1
      # 3. placer la page d'accueil comme premier element de la liste de tuples
      tuples[0], tuples[counter] = tuples[counter], tuples[0]
      # 4. reconvertir la liste de tuples en tableau
      pages_dict = dict(tuples)

    # Parcourir tous les slots de chaque page et affecter la page destination au 1er slot sans destination.
    for page in pages_dict.values():
      if page.get_name() != extra_page.get_name():
        for row in range(1, page.get_row_size()):
          for col in range(1, page.get_col_size()):
            slot = page.get_slot(row, col)
            if slot:
              if not slot.get_page_destination():
                # slot.set_page_destination(extra_page)  ****
                new_slot = Slot(slot.get_word(), False, extra_page)
                page.set_slot(new_slot, row, col)

                #m-à-j le tableau d'attributes
                for key, picto in core_voc_dict.items():
                  if picto[0] == slot.get_word() and picto[1] == row and picto[2] == col and picto[3] == page.get_name():
                    
                    picto[4] = extra_page.get_name()
                                  
                # print([(k,p) for k,p in core_voc_dict.items() if p[3] == 'accueil'])
                return page

  def __generate_random_grid(self, input_file):
    '''Generate a random grid from a .txt input file (corpus)

    :param input_file: source text file containing the corpus
    :type input_file: `.txt` file
    :raises Exception: Incorrect file format !
    '''
    #Vocabulary of the corpus
    rawVoc = []

    #The source file is a '.txt' file
    if(input_file.endswith('.txt')):

      #Source file opening
      with open(input_file,"r") as rawFile:

        #For each line in the file, split the line
        for line in rawFile:
          sentence = line.strip()
          splittedLine = sentence.split(" ")

          #For each word in the splitted line, store it in the vocabulary of the corpus
          for word in splittedLine:
            rawVoc.append(word)
            
    #The source file is not a '.txt' file
    else:
      raise Exception("Incorrect file format !")

  def __create_grid(self, input_file):
    '''Crée une grille à partir d'un fichier texte ou d'un tableau d'attributes

    :param input_file: fichier/tableau source contenant toute l'information d'une grille 
    :type input_file: fichier `.csv` en format `Augcom` (voir le repo du projet pour plus d'information), 
    ou tableau d'attributes décrivant chaque pictogramme (format: {`id_picto`:[`nom`,`ligne`,`colonne`,`page`, `page_dest`]})    
    :raises Exception: exception d'entrée incompatible
    '''

    #référence pour le calcul de row_size, col_size et destination
    last_id = None

    # si l'entrée est un dictionaire de pictogrammes
    if isinstance(input_file, dict):
      # print("Grille créée à partir d'un dictionaire de pictogrammes")
      
      self.__core_voc = dict(input_file)

    # si l'entrée est un fichier .csv en format Augcom
    elif input_file.endswith('.tsv'):
      # print("Grille créée à partir du fichier " + input_file)
    
      # Fichier brut à traiter
      with open(input_file, "r") as rawFile:

        #Traitement du fichier source
        for lines in rawFile:
          lines = lines.lower()
          sentence = lines.strip()
          col = sentence.split("\t")

          # On gére le problème des lignes semi-vides créées par les liens entre les répertoires
          if len(col) > 4:
            
            word = col[0]
            row = int(col[1])
            column = int(col[2])
            page = col[3]			
            id = col[4]

            # enregistrer le mot, les coordonnées, la page actuelle et la destination de chaque pictogramme
            self.__core_voc[id] = [word, row, column, page, None]
            
            last_id = id

          # Nous récupérons les liens entre les répertoires
          elif len(col) > 1:            
            pointed_link = col[1]            			
            self.__core_voc.get(last_id)[4] = pointed_link

    else:
      raise Exception('Entrée incompatible. Seul tableaux d attributes (dict) ou fichiers .csv (format AUGCOM) sont acceptés')

    self.__add_core_voc()


  def __add_core_voc(self):
    '''Mettre en place la structure de la grille à partir de son tableau d'attributes
    
    Crée des pages et des slots et les affecte en suivant le tableau d'attributes'''
    
    #parcourir le tableau d'attributes and extraire l'information
    for picto in self.__core_voc.values():
      word = picto[0]
      row = picto[1]
      col = picto[2]
      page_name = picto[3]
      dest_name = picto[4]

      # créer la page contenant le picto s'il n'existe pas
      if page_name in self.__pages:
        page = self.__pages.get(page_name)
      else:		  
        page = self.__add_page(page_name)

      # créer la page de destination s'il n'existe pas    
      if dest_name:
        if dest_name in self.__pages:
          destination = self.__pages.get(dest_name)
        else:			
          destination = self.__add_page(dest_name)          
      else:
        destination = None

      # créer un slot et l'ajouter dans la bonne page et position
      slot = Slot(word, True, destination)    
      page.set_slot(slot, row, col)


  def cross_pages(self, page1, page2, parent=None):
    '''Croise deux pages et toutes les sous-pages analogues reliées entre elles 

    :param page1: première page à croiser
    :type page1: classe: `Page`
    :param page2: deuxième page à croiser
    :type page2: classe: `Page`
    :param parent: page de référence pour mettre en place les pictogrammes de retour. Cette page fait un appel récursive, defaults to None
    :type parent: classe: `Page`, optional
    :return: renvoie 3 choses: Un tableau contenant les attributes des pictos dans la page résultante,
     la page résultante et un tableau contenant les pictos non affectés à la page résultante lors du croissement
    :rtype: [type]
    '''

    # obtenir la taille des pages    
    row_size = self.get_row_size()
    col_size = self.get_col_size()
    
    # sufixe pour rendre unique le nom de chaque page (pas implémenté)
    new_page_name_suffix = random.randint(0,10000)

    # tableau de tous les attributs des pictogrammes de la page résultante
    attributes = {}

    # tableau des pictogrammes non affectés lors de la fusion
    unallocated_pictos = {}

    # tableau pour stocker les pictos non affectés dans les appels récursives
    unalloc = {}

    # CAS 1: Aucune page n'existe
    # ============================
    if (not page1) and (not page2):
      # print('Rien a croiser, fin de la fonction')
      
      return {}, None, unalloc
    
    # CAS 2: seul page1 existe
    # ============================
    if page1 and (not page2):
      result_page = copy.deepcopy(page1)
      picto_dict = result_page.get_pictograms()

      # m-à-j du picto_dict
      for id, picto1 in picto_dict.items():
            # réviser les duplicatas
            while id in attributes:
              id = f'{id}*'
            
            attributes[id] = picto1

      for picto in picto_dict.values():
        # chercher et m-à-j le picto de retour.
        if (picto[0] == 'retour_r') and (picto[1] == row_size - 1) and (picto[2] == col_size - 1):
          if parent:
            picto_dict[f'retour_r@{result_page.get_name()}'][4] = parent.get_name()
            
        else:
          slot = result_page.get_slot(picto[1], picto[2])
          dest = slot.get_page_destination()

          #déterminer (recursivement) les pictos liés à la destination de chaque slot
          attribs, selected_dest_page, unalloc = self.cross_pages(dest, None, result_page)

          # m-à-j de attributes
          for pict_id, picto2 in attribs.items():
            # réviser les duplicatas
            while pict_id in attributes:
              pict_id = f'{pict_id}*'
            
            attributes[pict_id] = picto2  
      
      return attributes, result_page, {}      
    
    # CAS 3: seul page2 existe
    # ============================
    if page2 and (not page1):        
      result_page = copy.deepcopy(page2) 
      picto_dict = result_page.get_pictograms()

      # m-à-j du picto_dict
      for id, picto1 in picto_dict.items():
            # réviser les duplicatas
            while id in attributes:
              id = f'{id}*'
            
            attributes[id] = picto1

      for picto in picto_dict.values():
        # chercher et m-à-j le picto de retour.
        if (picto[0] == 'retour_r') and (picto[1] == row_size - 1) and (picto[2] == col_size - 1):
          if parent:
            picto_dict[f'retour_r@{result_page.get_name()}'][4] = parent.get_name()

        else:
          slot = result_page.get_slot(picto[1], picto[2])
          dest = slot.get_page_destination()

          #déterminer (recursivement) les pictos liés à la destination de chaque slot
          attribs, selected_dest_page, unalloc = self.cross_pages(None, dest, result_page)

          # m-à-j de attributes
          for pict_id, picto2 in attribs.items():
            # réviser les duplicatas
            while pict_id in attributes:
              pict_id = f'{pict_id}*'
            
            attributes[pict_id] = picto2  
      
      return attributes, result_page, {}

    # CAS 4: les deux pages existent
    # ============================
    if page1 and page2:

      # décider le nom du page à retenir
      if random.randint(0,1):
        new_page_name = page1.get_name()
      else:
        new_page_name = page2.get_name()

      # TO-DO: Vérifier si new_page_name existe déjà dans les pages selectionées. Deux solutions:  
      # - ajouter suffixe au nom de la page pour la differencier des pages de base
      # new_page_name += f'_{new_page_name_suffix}'
      # où
      # - Enregistrer les noms crées au fur et à mesure du croissement dans une liste, puis modifier légerement le nom si déjà dans la liste
      # # ?? 

      #page résultante
      result_page = Page(new_page_name, row_size, col_size)

      #sélectionner les pictos qui vont populer la page résultante
      for row in range(row_size):
        for col in range(col_size):
          slot_page1 = copy.deepcopy(page1.get_slot(row, col))
          slot_page2 = copy.deepcopy(page2.get_slot(row, col))
          random_selector = random.randint(0,1)

          # les deux pictogrammes existent
          if (slot_page1) and (slot_page2):
            dest_1 = slot_page1.get_page_destination()
            dest_2 = slot_page2.get_page_destination()

            if random_selector:
              selected_slot = slot_page1
              not_selected_slot = slot_page2
              page_name = page1.get_name()
              page_name_not_selected = page2.get_name()
              
            else:
              selected_slot = slot_page2
              not_selected_slot = slot_page1
              page_name = page2.get_name()
              page_name_not_selected = page1.get_name()
    
            #déterminer (recursivement) la destination du slot selectionné
            if (selected_slot.get_word() != 'retour_r'):              
              attribs, selected_dest_page, unalloc = self.cross_pages(dest_1, dest_2, result_page)
			      # picto de retour trouvé
            elif (row == row_size - 1) and (col == col_size - 1):
              attribs, selected_dest_page, unalloc = {}, parent, {}

            #garder les pictos non affectés --------------------------------------
            word_not_selected = not_selected_slot.get_word()
            if word_not_selected != 'retour_r':
              id_not_selected = f'{word_not_selected}@{page_name_not_selected}'

              #si deux pictos non affectés ont le même id, modifier légerement l'id de l'un des deux
              while id_not_selected in unallocated_pictos or id_not_selected in attributes:
                # '*' à la fin d'une id indiquera l'existence de 2 pictos differents avec la même mot et même nom de page 
                id_not_selected = f'{id_not_selected}*'            
                        
              unallocated_pictos[id_not_selected] = word_not_selected

          # seul le premier pictogramme existe
          elif slot_page1:
            selected_slot = slot_page1
            page_name = page1.get_name()

            if selected_slot.get_word() != 'retour_r':
              dest_1 = slot_page1.get_page_destination()
              attribs, selected_dest_page, unalloc = self.cross_pages(dest_1, None, result_page)            
            else:
              if parent:
                attribs, selected_dest_page, unalloc = {}, parent, {}              

          # seul le deuxième pictogramme existe
          elif slot_page2:
            selected_slot = slot_page2
            page_name = page2.get_name()

            if selected_slot.get_word() != 'retour_r':
              dest_2 = slot_page2.get_page_destination()
              attribs, selected_dest_page, unalloc = self.cross_pages(dest_2, None, result_page)            
            else:
              if parent:
                attribs, selected_dest_page, unalloc = {}, parent, {}
            
          # aucun des pictos n'existe pas
          else: 
            selected_slot = None            

          # --------------------------------------------------------------------------------------
          #m-à-j des attributes du pictogramme selectionné dans la page résultante
          if selected_slot:
            word = selected_slot.get_word()
            selected_slot = Slot(word, False, selected_dest_page)
            result_page.set_slot(selected_slot, row, col)

            #ajouter les pictos des pages de destination au tableau d'attributes
            attributes.update(attribs)

            #m-à-j le dict de pictos non affectés avec ceux des appels récursives
            unallocated_pictos.update(unalloc)

            if selected_dest_page:                
                dest_page_name = selected_dest_page.get_name()
            else:
              dest_page_name = None

            # id du picto selectionné
            id_selected = f'{word}@{page_name}'

            #si deux pictos ont le même id, modifier légerement l'id de l'un d'eux
            while id_selected in attributes or id_selected in unallocated_pictos:
              id_selected = f'{id_selected}*'
            
            attributes[id_selected] = [word, row, col, new_page_name, dest_page_name]

          # mettre en place le picto selectionné dans la page résultante 
          result_page.set_slot(selected_slot, row, col)     
    
    return attributes, result_page, unallocated_pictos


  def fusion_with(self, grid):
    '''Fusione aléatoirement les strutures analogues (pages) de deux grilles

    Fonction récursive. En partant des deux accueils, on compare chaque slot d'une page avec son analogue 
    dans l'autre page et choisit aléatoirement l'un d'entre eux.
    Par exemple, les slots situés à la position (2,3) dans les pages d'accueil de la première et la deuxième 
    grille sont utilisés pour définir le slot situé à (2,3) dans la page d'accueil de la grille résultante.
    Ainsi, pour chaque position il y a toujours un slot selectionné (ce qui va dans les pages de base de la 
    grille résultante) et un autre non-selectionné qui va dans des pages spécialement concues à ce propos (extra_pages).

    La grille résultante est une structure unique et indépéndante. Elle contient les pictogrammes des deux grilles
    originales.

    :param grid: la deuxième grille avec laquelle la grille actuelle va se fusioner
    :type grid: classe: `Grid`
    :return: une nouvelle grille avec une nouvelle structure 
    :rtype: classe: `Grid`
    '''

    # tableau d'attributes de la grille résultante contenant uniquement les pictos selectionnés
    attributes_dict = {}

    # tableau contentant tous les pictogrammes non selectionnés lors de la fusion
    unalloc_dict = {}

    # extraire la taille des grilles
    row_size = self.get_row_size()
    col_size = self.get_col_size()

    # extraire les pages d'accueil de chacune des grilles
    current_accueil = self.get_root_page() 
    foreing_accueil = grid.get_root_page()  

    # Fusioner les deux grilles à travers leurs pages d'accueil.   
    attributes_dict, result_page, unalloc_dict = self.cross_pages(current_accueil, foreing_accueil)    

    # Créer la structure de base de la grille résultante
    new_grid = Grid(attributes_dict, row_size, col_size)

    # remplir slots vides (pas de slot) avec les pictos non affectées
    for page in new_grid.get_page_dict().values():
      for row in range(1, row_size):
        for col in range(1, col_size):
          slot = page.get_slot(row, col)
          if not slot:            
            try:
              # renvoyer l'id du pictgramme non affecté suivant
              id_next_unalloc_picto = next(iter(unalloc_dict))

              #vérifier si l'id du picto non alloué existe déjà dans le tableau d'attributes de la grille (re-check)
              if id_next_unalloc_picto in new_grid.get_core_voc():
                new_id = f'{id_next_unalloc_picto}*'
                # ajouter des '*' jusqu'à ce que l'id soit unique
                while new_id in new_grid.get_core_voc():
                  new_id = f'{new_id}*'

                unalloc_dict[new_id] = unalloc_dict.pop(id_next_unalloc_picto)
                id_next_unalloc_picto = new_id

              unalloc_picto = unalloc_dict.pop(id_next_unalloc_picto)
              word = unalloc_picto
              slot = Slot(word, False, None)
              page.set_slot(slot, row, col)

              #m-à-j du dict d'attriburtes de la nouvelle grille
              new_grid.get_core_voc()[id_next_unalloc_picto] = [word, row, col, page.get_name(), None]     

            # unalloc_dict est vide         
            except:
              print('** fusion complète 1 **')
              return new_grid
    
    # gérer le cas où il y a plus de pictos non alloués que de slots vides.
    while len(unalloc_dict):
            
      # créer et ajouter une page extra pour les allouer
      extra_page_name = f'extra_{random.randint(0,10000)}'    
      extra_page = new_grid.add_new_page(extra_page_name)

      # choisir le picto connecté à la page extra. On parcours les pages en partant de l'accueil.
      origin_page = new_grid.update_leaf_picto(extra_page)    

      # mettre en place le picto de retour
      if origin_page:
        picto_retour = Slot('retour_r', False, origin_page)
        extra_page.set_slot(picto_retour, row_size - 1, col_size - 1)
        new_grid.get_core_voc()[f'retour_r@{extra_page_name}'] = ['retour_r', row_size - 1, col_size - 1, extra_page_name, origin_page.get_name()]
      
      # remplir slots vides de la PAGE EXTRA avec des pictos non affectées
      for row in range(1, row_size):
          for col in range(1, col_size):
            slot = extra_page.get_slot(row, col)
            # si le slot est vide
            if not slot:
              try:
                # renvoyer l'id du pictgramme non affecté suivant
                id_next_unalloc_picto = next(iter(unalloc_dict))

                #vérifier si l'id du picto non alloué existe dans le dict d'attributes de la grille
                # sinon, ajouter '*' à la fin de l'id répété pour en créér un id unique  
                if id_next_unalloc_picto in new_grid.get_core_voc():
                  new_id = f'{id_next_unalloc_picto}*'

                  while new_id in new_grid.get_core_voc():
                    new_id = f'{new_id}*'

                  unalloc_dict[new_id] = unalloc_dict.pop(id_next_unalloc_picto)
                  id_next_unalloc_picto = new_id

                unalloc_picto = unalloc_dict.pop(id_next_unalloc_picto)
                word = unalloc_picto
                slot = Slot(word, False, None)
                extra_page.set_slot(slot, row, col)

                #m-à-j du dict d'attriburtes de la nouvelle grille
                new_grid.get_core_voc()[id_next_unalloc_picto] = [word, row, col, extra_page.get_name(), None]              
              except:
                print('** fusion complète 2 **')                
                return new_grid
                
    return new_grid


  # TO-DO: ne fonctionne pas, à déboger 
  def shuffle(self):
    '''Mélange les pictogrammes à l'intérieure de chaque page de la grille

    Change uniquement la distribution spaciale des pictogrammes d'une page. 

    :raises Exception: capacité de la page dépassé
    :return: nouvelle grille 
    :rtype: classe: `Grid`
    '''

    # copier le tableau d'attributes de la grille originale
    core_voc_copy = copy.deepcopy(self.get_core_voc())

    # new_grid_core_voc = new_grid.get_core_voc()
    row_size = self.get_row_size()
    col_size = self.get_col_size()

    #créer liste de coordoneées de slots
    all_coords = [(i,j) for i in range(1, row_size) for j in range(1, col_size)]
    
    #omettre le picto dans le coin en bas à droite (retour, plus, etc) 
    all_coords.pop()

    for page_name in self.get_page_dict():
      # liste de toutes les coordonnées sauf (row_size-1, col_size-1)
      coords_list = list(all_coords) 
      # 
      info = []

      #mélange la liste
      random.shuffle(coords_list)
      
      for id, picto in self.get_core_voc().items():
        
        # choisir pictos dans la même page. Ne tenir pas compte des pictos en ligne/col = 0. 
        if (picto[3] == page_name) and (picto[1] != 0) and (picto[2] != 0):
          info.append((id, picto))
          if (picto[1] != row_size-1) or (picto[2] != col_size-1):     
            
            try:          
              row, col = coords_list.pop()
            except:              
              raise Exception('Le nombre de pictogrammes dépasse la capacité de la page. Valider tableau d attributes')
            
            #affecter les nouvelles coordonnées aux pictos de la pag courante
            core_voc_copy[id][1] = row
            core_voc_copy[id][2] = col
    
    return Grid(core_voc_copy, row_size, col_size)


  def to_graph(self):
    '''Génére un graphe décrivant la structure de la grille

    :return: un graphe dirigé
    :rtype: classe: `networkx.DiGraph`
    '''

    nodes = set([])
    edges = set([])
    for key,page in self.__pages.items():
      nodes.add(key)
      slots = page.get_slot_list()
      for items in slots:
        for slot in items:
          if slot != None:
            dest = slot.get_page_destination()
            if dest != None:
              dest = dest.get_name()
              edges.add((key, dest))
    
    G=nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    nx.draw(G,with_labels=True)
    # plt.savefig("grid_graph.png") # save as png
    plt.show() # display

    return G


  def to_text(self, output_name='grid_text.csv'):
    '''Crée un fichier texte (.csv) décrivant la grille en format AUGCOM.

    Voir le repo du projet pour plus d'information sur le format Augcom.

    :param output_name: le nom du fichier résultant, defaults to 'grid_text.csv'
    :type output_name: chaîne de charactères, optional
    '''

    print("output file is " + output_name)
    print()
    sorted_attrib_dict = {}

    # trier le dict d'attributes par nom de page
    for page_name in self.get_page_dict():     
      for picto_id, attributes in self.get_core_voc().items():
        if attributes[3] == page_name:
          sorted_attrib_dict[picto_id] = self.get_core_voc().get(picto_id)       

    # Fichier résultant
    with open(output_name, "w") as text_file:
      for picto_id, attributes in sorted_attrib_dict.items():
        print(f'{attributes[0].upper()}\t{attributes[1]}\t{attributes[2]}\t{attributes[3]}\t{picto_id}', file=text_file) 
        if attributes[4]:
          print(f'\t\t\t{picto_id}\t{attributes[4]}', file=text_file)


  def __str__(self):
    '''Méthode d'affichage 1

    :return: renvoie une représentation lisible de la structure de la grille
    :rtype: chaîne de charactères
    '''

    s = 'grid : {\n'
    for page in self.__pages.values():
      s+= str(page) + '\n'
    s += '}\n'
    return s

     
  def display(self, name='default'):
    '''Méthode d'affichage 2

    Génére une image detaillé et intuitive de la structure de la grille. Il utilise Graphviz et le language DOT.
    Il export automatiquement l'image en format png au répértoire actuel 

    :param name: le nom du fichier image produit, defaults to 'default'
    :type name: chaîne de charactères, optional
    :return: renvoie un graphe dirigé
    :rtype: classe: `networkx.DiGraph`
    '''

    graph = Digraph(comment='Test', node_attr={'shape': 'record'}) #, 'fixedsize': 'true', 'width':'4', 'height':'2'})
    row_size = self.get_row_size()
    col_size = self.get_col_size()
    slot_index = 0

    for page_name,page in self.get_page_dict().items():
      
      attribute_string = '{ '
      separator_1 = ''
      for row in range(0, row_size):
        separator_2 = ''
        attribute_string += f'{separator_1}' + ' { '
        for col in range(0, col_size):
          slot_index  = row * col_size + col
          slot = page.get_slot(row, col)

          if slot:
            word = slot.get_word()
            dest = slot.get_page_destination()

            #ajouter lien entre picto directoire et la page correspondante 
            if dest:              
              graph.edge(f'{page_name}:{slot_index}', f'{dest.get_name()}')
          elif row == 0 and col == 0:
            word = page_name.upper()
          else:
            word = ''

          attribute_string += f'{separator_2}<{slot_index}>{word} '
          separator_2 = '|'

        separator_1 = '|'
        attribute_string += '} '
      attribute_string += ' }'

      #créer noeud 
      graph.node(f'{page_name}', f'{attribute_string}')

    # rendre l'image et l'export au format png  
    graph.render(filename=name,format='png')

    return graph