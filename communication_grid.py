import random
import copy
import math
import csv
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

      self.word = copy.copy(word)
      self.row = row
      self.col = col
      self.page_name = page_name
      self.id = id

    def get_pictogram_in_list(self):
      '''Getter for the entire list of attribute
      
      :return: Returns the list of all attributes of the pictogram
      :rtype: list
      '''
      
      return [self.word,self.row,self.col,self.page_name,self.id]

    def set_word(self, word):
        '''Setter. Set the word of the pictogram
        
        :word: word to set
        :type word: string   
        '''

        self.word = word

    def __str__(self):
        '''Display the pictogram information (text)
        
        :return: Return the pictogram information
        :rtype: string
        '''

        return f'"{self.word}",{self.row},{self.col},"{self.page_name}","{self.id}"'


class Slot():
    '''Smallest element of the grid. Representing one pictogram.
    
    Can contain a pictogram or be empty (None)

    :pictogram: corresponding pictogram
    :type: classe: `Pictogram`
    :page_destination: Destination page of the pictogram (if any). Can be null (None)
    :type page_destination: class: `Page`
    '''

    def __init__(self, pictogram, page_destination):        
        '''Constructor        
        '''        
        self.pictogram = copy.copy(pictogram)
        self.page_destination = copy.copy(page_destination)
        

    def get_word(self):
        '''Getter
        
        :return: Returns the corresponding word of the slot
        :rtype: string       
        '''

        return self.pictogram.word


    def set_pictogram(self, pictogram):
        '''Setter. Set the pictogram of the slot
        
        :pictogram: word to set
        :type pictogram: class: `Pictogram` 
        '''

        self.pictogram = pictogram

    def set_word(self, word):
        '''Setter. Set the word of the slot
        
        :word: word to set
        :type word: string   
        '''

        self.pictogram.set_word(word)

    def set_page_destination(self, page):
        '''Setter. Set the destination page of the slot
        
        :page: destination page to set
        :type page: class: `Page`        
        '''

        self.page_destination = page

    def __str__(self):
        '''Display the slot (text)
        
        :return: Return the slot information
        :rtype: string
        '''

        dest = self.page_destination
        if dest:
            dest = self.page_destination.name

        return f'{self.word}({dest})'


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

        self.name = name
        self.row_size = row_size
        self.col_size = col_size
        #Full indicator (False, the page is not full)
        self.full = False
        #List of slots of the page
        self.slots = []
        #Fill the page of empty slots
        self.empty_fill()

        #Position of the next empty slot (if any)
        self.last_row = 0
        self.last_col = 0


    def empty_fill(self):
      '''Initialize each slots of the page as empty (None)'''

      self.slots = []
      for i in range(0, self.row_size) :
        self.slots.append([None])
        for j in range(0, self.col_size) :
          self.slots[i].append(None)


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

      if (num_row >= self.row_size) or (num_col >= self.col_size):
        print(f'row={num_row}, col={num_col}')
        print(f'row_size={self.row_size}, col_size={self.col_size}')
                
        raise Exception('Error: slot row or col out of bounds') 

      old_slot = self.slots[num_row][num_col]
      self.slots[num_row][num_col] = slot

      return old_slot


    def set_name(self, name):
      '''Setter. Set the name of the page. 

      :param name: page name to set
      :type name: string
      :return: return the affected name
      :rtype: string
      '''
      self.name = name

      return name

    def get_slot(self, num_row, num_col):
      '''Getter. 

      :return: returns the slot at the position `(num_row, num_col)` 
      :rtype: class: `Slot`
      '''

      return self.slots[num_row][num_col]

    def get_empty_slot(self):
      '''Getter.

      :return: returns the next empty slot coordinates of the page at position `(last_row,last_col)`, if any.
      :rtype: integer,integer
      '''

      #End of the row
      if(self.last_col == self.col_size) : 
        self.last_col = 0
        self.last_row += 1

      if(self.full == False):
        return self.last_row,self.last_col
        
      else:
        return -1,-1
    
    def get_pictograms(self):
      '''Get all pictograms of the page.

      Build the list of pictograms within the page. 

      :return: returns a list of pictograms.
      :rtype: class: Pictogram []
      '''

      #List of pictograms to return
      pictograms = []
      #For each pictogram in the page
      for row in range(0, self.row_size):
        for col in range (0, self.col_size):
          slot = self.slots[row][col]
          #If not empty, we add it to the list
          if(slot != None):
            pictograms.append(slot.pictogram)

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
      return self.slots[num_row][num_col] == None


    def page_is_full(self):
      '''Returns True if the page is full (not empty slot), else returns False

      :return: returns a boolean
      :rtype: boolean
      '''

      #If the full indicator is True, the page is full
      if (self.full):
        return True

      #Else, we check if we find an empty slot in the whole page
      for row in range(0, self.row_size):
        for col in range (0, self.col_size):
          
          #Empty slot found
          if self.slots[row][col] == None:
            return False

      #If no empty slot found, the page is full
      self.full = True
      return True


    def add_pictogram(self, pictogram, dest=None) :
      '''Generate and add a new pictogram in the next free slot of the page (if any).

      :param pictogram: pictogram
      :type: class: Pictogram
      :param dest: destination page of the pictogram, defaults to None
      :type dest: classe: `Page`, (optional)
      :return: returns the name of the word if it was possible, null if not.
      :rtype: string
      '''

      #End of the row
      if(self.last_col == self.col_size) : 
        self.last_col = 0
        self.last_row += 1

      #End of the table (table is full)
      if(self.last_row == self.row_size) :
        self.full = True
        print("Failed to add word <", pictogram.word, ">. The table is full.")

        return None

      #If the slot is empty
      if(self.slot_is_free(self.last_row,self.last_col)):
        s = Slot(pictogram,dest)
        self.slots[self.last_row][self.last_col] = s
        self.last_row
        self.last_col += 1

        return pictogram.word
      
      self.last_row
      self.last_col += 1

    def __str__(self):
      '''Display a page (text)

      :return: return the structure of the page in a visible format
      :rtype: string
      '''

      s = "Page: " + self.name + "\n("
      for i in range(0, self.row_size) : 
        for j in range(0, self.col_size) :
          s+=str(self.slots[i][j])
          s+=", "
        if(i < self.row_size - 1):
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

    self.row_size = row_size
    self.col_size = col_size
    self.picto_voc = {}
    self.root_name = root_name
    self.pages = {}
    self.pageCounter = 0     
    self.randomizer = randomizer
    self.dynamic_size = dynamic_size
    self.generate_grid(input_file)

  def get_root_page(self):
    '''Get the root page (named by defaylt : `accueil`)

    :return: returns the root page. 
    :rtype: class: `Page`
    '''

    return self.pages.get(self.root_name)
  
  def get_page_names(self):
    '''Returns the list of page names within the grid.

    :return: list of names.
    :rtype: string []
    '''

    return self.pages.keys()


  def get_page(self, name):
    '''Returns the page with the name : `name` 

    :param name: name of the page to get.
    :type name: string
    :return: concerned page.
    :rtype: class: `Page`
    '''

    return self.pages.get(name) 

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

    return self.add_page(name)


  def add_page(self, name_page):
    '''Add a new page to the grid

    :param name: name of the new page
    :type name: string
    :return: new page
    :rtype: classe: `Page`
    '''
    
    page = Page(name_page, self.row_size, self.col_size)    
    self.pages[name_page] = page
    self.pageCounter += 1 

    return page

  
  def generate_grid(self,input_file):
    '''Encapsulation function.
    Generate a grid from a file.

    :param input_file: source file
    :type input_file: file
    :raises Exception: Not accepted file format !
    '''

    #'AugCom' file (dictionary)
    if isinstance(input_file, dict):
      self.generate_grid_dict(input_file)

    #'.csv' file
    elif(isinstance(input_file, list) and input_file.endswith('.csv')):
      self.load_grid_csv(input_file)

    #'.txt' file
    elif(input_file[0].endswith('.txt')):
      self.generate_grid_txt(input_file)

    #File format not accepted
    else:
      raise Exception("Not accepted file format !")


  def generate_grid_txt(self, corpus):
    '''Generate a grid from a .txt corpus

    :param corpus: source text file list containing the corpus
    :type corpus: `.txt` file list
    '''
    #Get the vocabulary of the corpus
    rawVoc = get_vocabulary_from_corpus(corpus)

    #If the size of the grid is dynamic
    if(self.dynamic_size == True):
      self.row_size = int(math.ceil(math.sqrt(len(rawVoc))))
      self.col_size = int(math.ceil(math.sqrt(len(rawVoc))))

    #Creating the root page   
    self.add_new_page(self.root_name)
    page = self.get_root_page()
    pageName = page.name

    #Transform each word into a pictogram in the page
    for i in range(len(rawVoc)):

      #Random generation
      if(self.randomizer):
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
          self.picto_voc[id] = picto.get_pictogram_in_list()

          # Create the slot and add it to the page
          page.add_pictogram(picto,None)

  def load_grid_csv(self, input_file):
    '''Load a grid from a .csv corpus

    :param input_file: source csv file
    :type input_file: `.csv` file
    '''

    #Get the vocabulary from the csv file
    self.picto_voc = get_vocabulary_from_csv(input_file)
    #Add the core voc to the grid
    self.add_picto_voc()

  def generate_grid_dict(self, input_file):
    '''Generate a grid from a dictionary input file with (format: {`id_picto`:[`word`,`row`,`col`,`page`, `page_dest`]}.

    :param input_file: source dictionary text file containing a pictogram grid.
    :type input_file: `Augcom` file
    :raises Exception: Incorrect file format !
    '''
    #If the input is a dictionary of pictograms.
    if isinstance(input_file, dict):
      
      #Copy of the dictionary in the picto_voc.
      self.picto_voc = input_file

    #The source file is not a 'AugCom' file (dictionary)
    else:
      raise Exception("Incorrect file format !")

    #Generate the entire grid and its pages and slots from the core vocabulary
    self.add_picto_voc()


  def add_picto_voc(self):
    '''From the initial grid (tsv format) or a dictionary, set the entire grid and all its pages.
    
    Generates pages and slots of the grid following the file format (csv,tsv) or the dictionary'''

    #If the size of the grid is dynamic, resize the grid size
    if(self.dynamic_size == True):
      self.row_size = int(math.ceil(math.sqrt(len(self.picto_voc.values()))))
      self.col_size = int(math.ceil(math.sqrt(len(self.picto_voc.values()))))
    
    #Exploring the entire core vocabulary to store its pictogram
    for picto in self.picto_voc.values():
      word = picto[0]
      row = picto[1]
      col = picto[2]
      page_name = picto[3]
      dest_name = picto[4]

      # If the corresponding page of the pictogram does not exist, create it.
      if page_name in self.pages:
        page = self.pages.get(page_name)
      else:		  
        page = self.add_page(page_name)

      # Create the destination page if it does not exist. 
      if dest_name != str(word) + "@" + str(page_name):
        if dest_name in self.pages:
          destination = self.pages.get(dest_name)
        else:			
          destination = self.add_page(dest_name)          
      else:
        destination = None

      final_picto = Pictogram(word,row,col,page_name,destination)
      # Create the slot and add it to the page
      page.add_pictogram(final_picto,destination)

  #=========================================================================================================================

  # PRINT AND DISPLAY METHODS OF THE GRID
  #--------------------------------------------------------------


  def to_csv(self,output_file = "default.csv"):

    #Opening the csv file
    f = open(output_file,"w",encoding = "utf-8",newline = '')

    #Initialization of the writer
    writer = csv.writer(f)
    
    #Get the vocabulary (the grid)
    header = ['word','row','col','page','identifier']
    writer.writerow(header)
    voc = self.picto_voc

    #Write each row
    for picto in voc.values():
      writer.writerow(picto)
    
    f.close()

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
    for page_name in self.pages:     
      for picto_id, attributes in self.picto_voc.items():
        if attributes[3] == page_name:
          sorted_attrib_dict[picto_id] = self.picto_voc.get(picto_id)       

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
    for page in self.pages.values():
      s+= str(page) + '\n'
    s += '}\n'
    return s