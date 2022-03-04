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
from graphviz import Digraph

import networkx as nx
from networkx import *

from utils import *

class Pictogram:
    '''Object that will be stored in a slot. It contains several informations.

    :word: Corresponding word of the pictogram
    :type word: string
    :row: Row of the pictogram (in the page)
    :type row: integer
    :col: Col of the pictogram (in the page)
    :type col: integer
    :page_name: Page holding the pictogram
    :type page_name: string
    :id: Identifier of the pictogram
    :type id: string
    '''

    def __init__(self,word,row,col,page_name,id):
      '''Constructor
      '''

      self.__word = copy.copy(word)
      self.__row = row
      self.__col = col
      self.__page_name = page_name
      self.__id = id

    def get_word(self):
      '''Getter for word
      
      :return: Returns the corresponding word of the pictogram
      :rtype: string
      '''

      return self.__word
    
    def get_row(self):
      '''Getter for row
      
      :return: Returns the row position of the pictogram in its page
      :rtype: integer
      '''

      return self.__row

    def get_col(self):
      '''Getter for col
      
      :return: Returns the col position of the pictogram in its page
      :rtype: integer
      '''

      return self.__col
    
    def get_page_name(self):
      '''Getter for page name
      
      :return: Returns the name of the corresponding page of the pictogram
      :rtype: string
      '''
      return self.__page_name

    def get_id(self):
      '''Getter for the identifier of the pictogram
      
      :return: Returns the id of the pictogram
      :rtype: integer
      '''
      return self.__id

    def get_pictogram_in_list(self):
      '''Getter for the entire list of attribute
      
      :return: Returns the list of all attributes of the pictogram
      :rtype: list
      '''
      
      return [self.get_word(),self.get_row(),self.get_col(),self.get_page_name(),self.get_id()]

    def set_word(self, word):
        '''Setter. Set the word of the pictogram
        
        :word: word to set
        :type word: string   
        '''

        self.__word = word

    def __str__(self):
        '''Display the pictogram information (text)
        
        :return: Return the pictogram information
        :rtype: string
        '''

        return f'"{self.__word}",{self.__row},{self.__col},"{self.__page_name}","{self.__id}"'


class Slot():
    '''Smallest element of the grid. Representing one pictogram.
    
    Can contain a pictogram or be empty (None)

    :pictogram: corresponding pictogram
    :type: classe: `Pictogram`
    :is_core: True if the pictogram belongs to the vocabulary core, False if not. 
    :type is_core: boolean
    :page_destination: Destination page of the pictogram (if any). Can be null (None)
    :type page_destination: class: `Page`
    '''

    def __init__(self, pictogram, is_core, page_destination):        
        '''Constructor        
        '''        
        self.__pictogram = copy.copy(pictogram)
        self.__is_core = copy.copy(is_core)
        self.__page_destination = copy.copy(page_destination)

    def get_pictogram(self):
        '''Getter
        
        :return: returns the corresponding pictogram of the slot
        :rtype: class: ``Pictogram`
        '''
        return self.__pictogram
        

    def get_word(self):
        '''Getter
        
        :return: Returns the corresponding word of the slot
        :rtype: string       
        '''

        return self.__pictogram.get_word()

    def get_is_core(self):
        '''Getter

        :return: Returns the boolean `is_core` of the slot
        :rtype: boolean        
        '''

        return self.__is_core

    def get_page_destination(self):
        '''Getter
        
        :return: Returns the destination page of the slot
        :rtype: class: `Page`        
        '''

        return self.__page_destination


    def set_pictogram(self, pictogram):
        '''Setter. Set the pictogram of the slot
        
        :pictogram: word to set
        :type pictogram: class: `Pictogram` 
        '''

        self.__pictogram = pictogram

    def set_word(self, word):
        '''Setter. Set the word of the slot
        
        :word: word to set
        :type word: string   
        '''

        self.__pictogram.set_word(word)

    def set_page_destination(self, page):
        '''Setter. Set the destination page of the slot
        
        :page: destination page to set
        :type page: class: `Page`        
        '''

        self.__page_destination = page

    def __str__(self):
        '''Display the slot (text)
        
        :return: Return the slot information
        :rtype: string
        '''

        dest = self.__page_destination
        if dest:
            dest = self.__page_destination.get_name()

        return f'{self.get_word()}({dest})'


class Page():
    '''A page is a 2D arrangement of slots with a fixed size

    :param name: name of the page
    :type name: string
    :param row_size: height of the page (number of lines)
    :type row_size: integer
    :param col_size: width of the page (number of columns)
    :type col_size: integer
    '''

    def __init__(self, name, row_size, col_size):
        '''Constructor'''  

        self.__name = name
        self.__row_size = row_size
        self.__col_size = col_size
        #Full indicator (False, the page is not full)
        self.__full = False
        #List of slots of the page
        self.__slots = []
        #Fill the page of empty slots
        self.__empty_fill()

        #Position of the next empty slot (if any)
        self.__last_R = 0
        self.__last_C = 0


    def __empty_fill(self):
      '''Initialize each slots of the page as empty (None)'''

      self.__slots = []
      for i in range(0, self.__row_size) :
        self.__slots.append([None])
        for j in range(0, self.__col_size) :
          self.__slots[i].append(None)


    def set_slot(self, slot, num_row, num_col):
      '''Setter. Add the Slot `slot` at the position `num_row` and `num_col in the page.

      :param slot: slot to set
      :type slot: class `Slot`
      :param num_row: number of the row
      :type num_row: integer
      :param num_col: number of the column
      :type num_col: integer
      :raises Exception: Index out of bound.
      :return: return the old slot
      :rtype: class `Slot`
      '''

      if (num_row >= self.__row_size) or (num_col >= self.__col_size):
        print(f'row={num_row}, col={num_col}')
        print(f'row_size={self.__row_size}, col_size={self.__col_size}')
                
        raise Exception('Error: slot row or col out of bounds') 

      old_slot = self.__slots[num_row][num_col]
      self.__slots[num_row][num_col] = slot

      return old_slot


    def set_name(self, name):
      '''Setter. Set the name of the page. 

      :param name: page name to set
      :type name: string
      :return: return the affected name
      :rtype: string
      '''
      self.__name = name

      return name

    
    def get_name(self):
      '''Getter. 

      :return: returns the name of the page.
      :rtype: string
      '''

      return self.__name


    def get_row_size(self):
      '''Getter.

      :return: returns the height of the page.
      :rtype: integer
      '''

      return self.__row_size


    def get_col_size(self):
      '''Getter. 

      :return: returns the width of the page.
      :rtype: integer
      '''

      return self.__col_size


    def get_slot(self, num_row, num_col):
      '''Getter. 

      :return: returns the slot at the position `(num_row, num_col)` 
      :rtype: class: `Slot`
      '''

      return self.__slots[num_row][num_col]

    def get_empty_slot(self):
      '''Getter.

      :return: returns the next empty slot coordinates of the page at position `(last_R,last_C)`, if any.
      :rtype: integer,integer
      '''

      #End of the row
      if(self.__last_C == self.__col_size) : 
        self.__last_C = 0
        self.__last_R += 1

      if(self.__full == False):
        return self.__last_R,self.__last_C
        
      else:
        return -1,-1


    def get_slot_list(self):
      '''Getter

      :return: returns the list of slots of the page.
      :rtype: list of slots
      '''

      return self.__slots
    

    def get_pictograms(self):
      '''Get all pictograms of the page.

      Build the list of pictograms within the page. 

      :return: returns a list of pictograms.
      :rtype: class: Pictogram []
      '''

      #List of pictograms to return
      pictograms = []
      #For each pictogram in the page
      for row in range(0, self.__row_size):
        for col in range (0, self.__col_size):
          slot = self.__slots[row][col]
          #If not empty, we add it to the list
          if(slot != None):
            pictograms.append(slot.get_pictogram())

      return pictograms


    def slot_is_free(self, num_row, num_col):
      '''Returns True if the slot (`num_row`, `num_col`) is free, else returns False.

      :param num_row: number of the row
      :type num_row: integer
      :param num_col: number of the column
      :type num_col: integer
      :return: returns a boolean
      :rtype: boolean
      '''
      return self.__slots[num_row][num_col] == None


    def page_is_full(self):
      '''Returns True if the page is full (not empty slot), else returns False

      :return: returns a boolean
      :rtype: boolean
      '''

      #If the full indicator is True, the page is full
      if (self.__full):
        return True

      #Else, we check if we find an empty slot in the whole page
      for row in range(0, self.__row_size):
        for col in range (0, self.__col_size):
          
          #Empty slot found
          if self.__slots[row][col] == None:
            return False

      #If no empty slot found, the page is full
      self.__full = True
      return True


    def add_pictogram(self, pictogram, core=False, dest=None) :
      '''Generate and add a new pictogram in the next free slot of the page (if any).

      :param pictogram: pictogram
      :type: class: Pictogram
      :param core: indicator if the pictogram should be part of the vocabulary core (False by default)
      :type core: boolean, (optional)
      :param dest: destination page of the pictogram, defaults to None
      :type dest: classe: `Page`, (optional)
      :return: returns the name of the word if it was possible, null if not.
      :rtype: string
      '''

      #End of the row
      if(self.__last_C == self.__col_size) : 
        self.__last_C = 0
        self.__last_R += 1

      #End of the table (table is full)
      if(self.__last_R == self.__row_size) :
        self.__full = True
        print("Failed to add word <", pictogram.get_word(), ">. The table is full.")

        return None

      #If the slot is empty
      if(self.slot_is_free(self.__last_R,self.__last_C)):
        s = Slot(pictogram, core, dest)
        self.__slots[self.__last_R][self.__last_C] = s
        self.__last_R
        self.__last_C += 1

        return pictogram.get_word()
      
      self.__last_R
      self.__last_C += 1

    def __str__(self):
      '''Display a page (text)

      :return: return the structure of the page in a visible format
      :rtype: string
      '''

      s = "Page: " + self.__name + "\n("
      for i in range(0, self.__row_size) : 
        for j in range(0, self.__col_size) :
          s+=str(self.__slots[i][j])
          s+=", "
        if(i < self.__row_size - 1):
          s+='\n'

      return s+')'

    
class Grid():
  '''Meta-class representing the whole structure of a pictogram grid system. 

  :param input_file: - file`.csv` in format `Augcom` 
                     or - table of attributes representing each pictogram : {`id_picto` : [`name`, `row`, `column`, `page`, `destination`]}
                     or - file `.txt` as a corpus.

  :type input_file: file / Dict
  :param row_size: height of each page of the grid.
  :type row_size: integer
  :param col_size: width of each page of the grid.
  :type col_size: integer
  :raises Exception: incompatible input file.
  :param root_name: name of the root page ("accueil" by default)
  :type root_name: string
  :param randomizer: If True, the generation of the grid will be random, else, it will follow the input file.
  :type randomizer: boolean
  '''

  def __init__(self, input_file, row_size = 5, col_size = 5, root_name = "accueil", randomizer = True, dynamic_size = True):
    '''Constructor'''

    self.__row_size = row_size
    self.__col_size = col_size
    self.__core_voc = {}
    self.__root_name = root_name
    self.__pages = {}
    self.__pageCounter = 0     
    self.__randomizer = randomizer
    self.__dynamic_size = dynamic_size
    self.__generate_grid(input_file)

  
  def get_root_name(self):
    '''Get the root page name of the grid

    :return: return the root page name
    :rtype: string
    '''

    return self.__root_name



  def get_root_page(self):
    '''Get the root page (named by defaylt : `accueil`)

    :return: returns the root page. 
    :rtype: class: `Page`
    '''

    return self.__pages.get(self.get_root_name())

  
  def get_nb_pages(self):
    '''Returns the number of pages of a grid.

    :return: total number of pages.
    :rtype: integer
    '''

    return self.__pageCounter
  

  def get_page_names(self):
    '''Returns the list of page names within the grid.

    :return: list of names.
    :rtype: string []
    '''

    return self.__pages.keys()


  def get_page(self, name):
    '''Returns the page with the name : `name` 

    :param name: name of the page to get.
    :type name: string
    :return: concerned page.
    :rtype: class: `Page`
    '''

    return self.__pages.get(name) 


  def get_page_dict(self):
    '''Returns the dictionary of all pages within the grid.

    :return: dictionnary of pages.
    :rtype: Dict (format: {`page_name`: chaine de charactères : `page`: classe `Page`})
    '''

    return self.__pages


  def get_core_voc(self):
    '''Return the core vocabulary of the grid (all pictograms).

    :return: list of pictograms.
    :rtype: Dict (format: {`id_picto`:[`nom`,`ligne`,`colonne`,`page`, `page_dest`]})
    '''

    return self.__core_voc


  def get_row_size(self):
    '''Returns the height of the grid.

    :return:number of rows.
    :rtype: integer
    '''

    return self.__row_size


  def get_col_size(self):
    '''Returns the width of the grid.

    :return:number of columns.
    :rtype: integer
    '''

    return self.__col_size

  def get_randomizer(self):
    '''Returns the randomizer of the grid.

    :return: randomizer.
    :rtype: boolean
    '''

    return self.__randomizer

  def get_dynamic_size(self):
    '''Returns if the grid has a dynamic size or not.

    :return: dynamic_size.
    :rtype: boolean
    '''

    return self.__dynamic_size

  def set_row_size(self,row_size):
    '''Setter. Set the row_size 

    :param: new row size of the grid
    :type row_size: integer
    '''

    self.__row_size = row_size

  def set_col_size(self,col_size):
    '''Setter. Set the col_size 

    :param: new col size of the grid
    :type col_size: integer
    '''

    self.__col_size = col_size

  
  def add_word_in_root(self, pictogram, dest=None):
    '''Add a new pictogram to the root page in the first empty slot.

    :param pictogram: pictogram to add
    :type pictogram: class: Pictogram
    :param dest: destination page of the pictogram, defaults to None
    :type dest: classe `Page`, (optional)
    '''

    root_page = self.get_root_page()
    if root_page.page_is_full() :

      print('root page is full')
      return

    root_page.add_pictogram(pictogram, dest=dest)

    return


  def add_new_page(self, name):
    '''Encapsulation function 

    Add a new page to the grid

    :param name: name of the new page
    :type name: string
    :return: new page
    :rtype: classe: `Page`
    '''

    return self.__add_page(name)


  def __add_page(self, name_page):
    '''Add a new page to the grid

    :param name: name of the new page
    :type name: string
    :return: new page
    :rtype: classe: `Page`
    '''
    
    page = Page(name_page, self.get_row_size(), self.get_col_size())    
    self.__pages[name_page] = page
    self.__pageCounter += 1 

    return page

  
  def __generate_grid(self,input_file):
    '''Encapsulation function.
    Generate a grid from a file.

    :param input_file: source file
    :type input_file: file
    :raises Exception: Not accepted file format !
    '''

    #'AugCom' file (dictionary)
    if isinstance(input_file, dict):
      self.__generate_grid_dict(input_file)

    #'.txt' file
    elif(input_file.endswith('.txt')):
      self.__generate_grid_txt(input_file)

    #'.csv' file
    elif(input_file.endswith('.tsv')):
      self.__generate_grid_csv(input_file)

    #File format not accepted
    else:
      raise Exception("Not accepted file format !")


  def __generate_grid_txt(self, input_file):
    '''Generate a grid from a .txt input file (corpus)

    :param input_file: source text file containing the corpus
    :type input_file: `.txt` file
    '''
    #Get the vocabulary of the corpus
    rawVoc = get_vocabulary_from_txt(input_file)

    #If the size of the grid is dynamic
    if(self.get_dynamic_size() == True):
      self.set_row_size(int(math.ceil(math.sqrt(len(rawVoc)))))
      self.set_col_size(int(math.ceil(math.sqrt(len(rawVoc)))))

    #Creating the root page   
    self.add_new_page(self.get_root_name())
    page = self.get_root_page()
    pageName = page.get_name()

    #Transform each word into a pictogram in the page
    for i in range(len(rawVoc)):

      #Random generation
      if(self.get_randomizer()):
        ridx = random.randint(0,len(rawVoc) - 1)
        word = rawVoc[ridx]
        rawVoc.pop(ridx)
      #Not random generation
      else:
        word = rawVoc[i]

      #If there is an empty slot in the page
      if page.page_is_full() == False:
          #Get the row and col of the next empty slot
          slot_row,slot_col = page.get_empty_slot()

          #Create the pictogram
          id = str(word)+"@"+str(pageName)
          picto = Pictogram(word,slot_row,slot_col,pageName,id)

          #Store the pictogram in the vocabulary
          self.__core_voc[id] = picto.get_pictogram_in_list()

          # Create the slot and add it to the page
          page.add_pictogram(picto,True,None)

  def __generate_grid_csv(self, input_file):
    '''Generate a grid from a .csv input file.

    :param input_file: source csv file containing a pictogram grid.
    :type input_file: `.csv` file
    :raises Exception: Incorrect file format !
    '''

    last_id = None

    #The source file is a '.csv' file
    if(input_file.endswith('.tsv')):

      #Source file opening
      with open(input_file,"r") as rawFile:

        #For each line in the file, split the line
        for lines in rawFile:
          lines = lines.lower()
          sentence = lines.strip()
          col = sentence.split("\t")

          #Get the pictogram
          if len(col) > 4:
            
            word = col[0]
            row = int(col[1])
            column = int(col[2])
            page_name = str(col[3])			
            id = col[4]

            picto = Pictogram(word,row,column,page_name,id)

            #Store the pictogram in the vocabulary
            self.__core_voc[id] = picto.get_pictogram_in_list()

            last_id = id

          #Get the link of the pictogram (directory pictogram)
          elif len(col) > 1:            
            pointed_link = col[1]            			
            self.__core_voc.get(last_id)[4] = pointed_link

    #The source file is not a '.txt' file
    else:
      raise Exception("Incorrect file format !")

    #Generate the entire grid and its pages and slots from the core vocabulary
    self.__add_core_voc()

  def __generate_grid_dict(self, input_file):
    '''Generate a grid from a dictionary input file with (format: {`id_picto`:[`nom`,`ligne`,`colonne`,`page`, `page_dest`]}.

    :param input_file: source dictionary text file containing a pictogram grid.
    :type input_file: `Augcom` file
    :raises Exception: Incorrect file format !
    '''
    #If the input is a dictionary of pictograms.
    if isinstance(input_file, dict):
      
      #Copy of the dictionary in the core_voc.
      self.__core_voc = input_file

    #The source file is not a 'AugCom' file (dictionary)
    else:
      raise Exception("Incorrect file format !")

    #Generate the entire grid and its pages and slots from the core vocabulary
    self.__add_core_voc()


  def __add_core_voc(self):
    '''From the initial grid (tsv format) or a dictionary, set the entire grid and all its pages.
    
    Generates pages and slots of the grid following the file format (csv,tsv) or the dictionary'''

    #If the size of the grid is dynamic, resize the grid size
    if(self.get_dynamic_size() == True):
      self.set_row_size(int(math.ceil(math.sqrt(len(self.__core_voc.values())))))
      self.set_col_size(int(math.ceil(math.sqrt(len(self.__core_voc.values())))))
    
    #Exploring the entire core vocabulary to store its pictogram
    for picto in self.__core_voc.values():
      word = picto[0]
      row = picto[1]
      col = picto[2]
      page_name = picto[3]
      dest_name = picto[4]

      # If the corresponding page of the pictogram does not exist, create it.
      if page_name in self.__pages:
        page = self.__pages.get(page_name)
      else:		  
        page = self.__add_page(page_name)

      # Create the destination page if it does not exist. 
      if dest_name != str(word) + "@" + str(page_name):
        if dest_name in self.__pages:
          destination = self.__pages.get(dest_name)
        else:			
          destination = self.__add_page(dest_name)          
      else:
        destination = None

      final_picto = Pictogram(word,row,col,page_name,destination)
      # Create the slot and add it to the page
      page.add_pictogram(final_picto,True,destination)

  #=========================================================================================================================

  # PRINT AND DISPLAY METHODS OF THE GRID
  #--------------------------------------------------------------

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