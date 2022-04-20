from hashlib import new
import math
import random
from utils import *
from PageTree import PageTreeNode

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
    :is_directory: Tells if the pictogram is a directory or not
    :type is_directory: boolean (False by default)
    '''

    def __init__(self,word,row,col,page_name,id,is_directory = False):
        '''Constructor
        '''

        self.word = word
        self.row = row
        self.col = col
        self.page_name = page_name
        self.id = id
        self.is_directory = is_directory
    
    def in_list(self):
        '''Get the pictogram in a list form
      
        :return: Returns the list of all attributes of the pictogram
        :rtype: list
        '''
        
        return [self.word,self.row,self.col,self.page_name,self.id]

    def __str__(self):
        '''Display the pictogram information (text)
        
        :return: Return the pictogram information
        :rtype: string
        '''
        if(self.is_directory == False):
            dir_info = "NOT DIRECTORY"
        else:
            dir_info = "DIRECTORY"
        return f'[{self.word} [{self.row},{self.col}] {self.page_name} {self.id}] : {dir_info}'



class Page():
    '''A page is a 2D arrangement of pictograms and is a node of the grid

    :param name: name of the page
    :type name: string
    :param row_size: height of the page (number of lines, 5 by default)
    :type row_size: integer
    :param col_size: width of the page (number of columns, 5 by default)
    :type col_size: integer
    '''

    def __init__(self, name, row_size = 5, col_size = 5):
        '''Constructor'''  

        self.name = name
        self.row_size = row_size
        self.col_size = col_size
        self.pictograms = dict()

        #Position of the next pictogram (if not full)
        self.next_row = 0
        self.next_col = 0

        #Full indicator (False, the page is not full)
        self.is_full = False

    def add_new_pictogram(self,word):
        '''Method to add a pictogram to the page'''

        #End of column
        if(self.next_col == self.col_size):
            self.next_col = 0
            self.next_row += 1

        #End of row
        if(self.next_row == self.row_size):
            self.is_full = True
            print("Page '"+self.name+"' is full, can not contain : '"+str(word)+"'")
            return self.is_full
        
        #Create the pictogram and add it to the page
        picto = Pictogram(word,self.next_row,self.next_col,self.name,word+"@"+self.name)
        self.pictograms.update({picto.word : picto})

        #Next position
        self.next_col += 1

        return self.is_full

    def __str__(self):
        '''Display the pictograms of the page (text)'''

        display = ""

        #Prepare each pictogram display in the final display
        for picto in self.pictograms.values():
            display = display + str(picto) + "\n"

        return f'{display}'



class Grid():
    '''Meta-class representing the whole structure of a pictogram grid system.

    :param input_file: - file`.csv`, existing grid
                     or - file `.txt` as a corpus.
    :type input_file: file (.csv or .txt)
    :param randomizer: If True, the generation of the grid will be random, else, it will follow the input file.
    :type randomizer: boolean (True by default)
    '''

    def __init__(self,input_file,root_name = "accueil",randomizer = True):
        '''Constructor''' 

        self.root_name = root_name
        self.page_tree = None
        self.pages = dict()
        self.randomizer = randomizer
        self.generate_grid(input_file)


    def generate_grid(self,input_file):
        '''Encapsulation function.
        Generate a grid from a file.

        :param input_file: source file
        :type input_file: file
        :raises Exception: Not accepted file format !
        '''

        #'.txt file'
        if(input_file[0].endswith(".txt")):
            self.generate_grid_from_txt(input_file)

    def generate_grid_from_txt(self,corpus):
        '''Generate a grid from a .txt corpus

        :param corpus: source text file list containing the corpus
        :type corpus: `.txt` file list
        '''

        #Get the vocabulary of the corpus
        voc = get_vocabulary_from_corpus(corpus)

        #Get the first ideal dimension for each page of the grid
        best_row_size = 3
        best_col_size = 3

        #Root page of the grid (first page)
        current_name = self.root_name
        current_page = Page(current_name,best_row_size,best_col_size)
        self.pages.update({current_name : current_page})

        #Creation of the page tree with the root page
        self.page_tree = PageTreeNode(self.root_name)
        parent = self.page_tree
    
        page_number = 0
        
        #Transform each word into a pictogram in the page
        for i in range(len(voc)):

            #Random generation
            if(self.randomizer):
                ridx = random.randint(0,len(voc) - 1)
                word = voc[ridx]
                voc.pop(ridx)
            #Not random generation
            else:
                word = voc[i]

            #If the current page is not full add the pictogram
            ret_full = current_page.add_new_pictogram(word)
            
            #If the current page is full, the pictogram was not added, create a new page
            if(ret_full == True):

                #New page
                current_name = "default"+str(page_number)
                current_page = Page(current_name,best_row_size,best_col_size)
                self.pages.update({current_name : current_page})

                #Adding to the page tree
                new_node = PageTreeNode(current_name)
                parent.insert_child(new_node)
                page_number += 1

                #Add the pictogram to the new page
                current_page.add_new_pictogram(word)

  #=========================================================================================================================

  # PRINT AND DISPLAY METHODS OF THE GRID
  #--------------------------------------------------------------

    def display_information(self):
        '''Method to display the general information of the grid'''

        #Grid display

        print("================GRID================\n")
        print("ROOT PAGE : ",self.root_name)
        self.page_tree.tree_display()
        print("\n====================================\n")

        #Pages display

        print("================PAGES===============\n")
        for p in self.pages.values():
            print(p.name,"("+str(p.row_size)+"x"+str(p.col_size)+")",", "+str(len(p.pictograms)),"pictograms")
        print("\n====================================")