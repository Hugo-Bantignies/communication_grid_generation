import math
import random
import csv
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
        
        if(self.is_directory):
            return [self.word,self.row,self.col,self.page_name,self.id,"DIR",self.id.split("@")[0]]
        else:
            return [self.word,self.row,self.col,self.page_name,self.id,"NO"]

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
        self.parent_picto = None

        #Position of the next pictogram (if not full)
        self.next_row = 0
        self.next_col = 0

        #Full indicator (False, the page is not full)
        self.is_full = False

    def get_words(self):
        '''Method to get the words of the page'''
        words = []

        #For each picto, get its word
        for picto in self.pictograms.values():
            if(picto.is_directory == False):
                words.append(picto.word)
        
        return words

    def add_word_to_pictogram(self,word,is_directory = False,warnings = True):
        '''Method to add a pictogram to the page from a word'''

        #End of column
        if(self.next_col == self.col_size):
            self.next_col = 0
            self.next_row += 1

        #End of row
        if(self.next_row == self.row_size):
            self.is_full = True
            if(warnings == True):
                print("Page '"+self.name+"' is full, can not contain : '"+str(word)+"'")
            return self.is_full
        
        #Create the pictogram and add it to the page
        picto = Pictogram(word,self.next_row,self.next_col,self.name,word+"@"+self.name,is_directory = is_directory)
        self.pictograms.update({picto.word : picto})

        #Next position
        self.next_col += 1

        return self.is_full
    
    def add_pictogram(self,pictogram):
        '''Method to add an existing pictogram to the page'''

        self.pictograms.update({pictogram.word : pictogram})
    
    def remove_pictogram(self,word):
        '''Method to remove a pictogram from the page'''

        #Remove the pictogram
        target = self.pictograms[word]
        self.pictograms.pop(word)

        #Update the position of each pictogram in the dictionary
        for picto in self.pictograms.values():

            if(target.row * self.col_size + target.col <= picto.row * self.col_size + picto.col):
                #Start of row
                if(picto.col - 1 < 0):
                    picto.col = self.col_size - 1
                    picto.row -= 1
                
                else:
                    picto.col -= 1

        #Update the position for the next pictogram
        if(self.next_col - 1 < 0):
            self.next_col = self.col_size - 1
            self.next_row -= 1
        else:
            self.next_col -= 1

        #If the page is empty
        if(self.next_row < 0):
            self.next_row = 0
    
    def swap_pictograms(self,picto_a,picto_b):
        '''Method to swap two pictograms in the page'''

        #Keep the information of the pictogram b
        tmp_row = picto_b.row
        tmp_col = picto_b.col

        #Swap
        picto_b.row = picto_a.row
        picto_b.col = picto_a.col

        picto_a.row = tmp_row
        picto_a.col = tmp_col

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

    def __init__(self,input_file,root_name = "accueil",randomizer = True,warnings = True,page_row_size = 5,page_col_size = 5):
        '''Constructor''' 

        self.root_name = root_name
        self.page_tree = None
        self.pages = dict()
        self.picto_voc = dict()
        self.nb_picto = 0

        #Dimension of the pages
        self.page_row = page_row_size
        self.page_col = page_col_size

        self.randomizer = randomizer
        self.warnings = warnings
        if(isinstance(input_file, list)):
            self.generate_grid(input_file)
        elif(input_file.endswith(".csv")):
            self.load_grid(input_file)
    
    def load_grid(self,input_file):
        
        #Opening the csv file
        f = open(input_file,"r",encoding = "utf-8",newline = '')

        #Initialization of the reader
        reader = csv.reader(f)

        #Building the pictogram list
        picto_list = []

        header = next(reader)
        next(reader)

        for row in reader:
            if(row[5] == "DIR"):
                picto_list.append(Pictogram(row[0],int(row[1]),int(row[2]),row[3],row[4],True))
            else:
                picto_list.append(Pictogram(row[0],int(row[1]),int(row[2]),row[3],row[4]))

        self.root_name = header[0]
        self.page_row = header[1]
        self.page_col = header[2]

        #Get the root page name
        self.page_tree = PageTreeNode(self.root_name)

        #Create the root page
        root_page = Page(self.root_name,self.page_row,self.page_col)
        self.pages.update({self.root_name : root_page})


        #Build pages
        for picto in picto_list:

            #New page
            if(picto.is_directory == True):
                parent = self.page_tree.find_node(picto.page_name)
                parent.insert_child(PageTreeNode(picto.word))

                new_page = Page(picto.word,self.page_row,self.page_col)
                self.pages.update({new_page.name : new_page})

        #Load the grid
        for picto in picto_list:

            if(picto.word in self.picto_voc):
                self.picto_voc[picto.word].append(self.page_tree.find_node(picto.page_name))
            else:
                self.picto_voc.update({picto.word : [self.page_tree.find_node(picto.page_name)]})

            self.pages[picto.page_name].add_pictogram(picto)

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

    def generate_grid_structure(self,voc):
        '''Generate an empty grid structure (tree and directory pictograms) from the vocabulary
        '''

        #Get the number of pictograms from the voc
        tmp_nb_picto = len(voc)

        #Get the number of pages / directories
        nb_pages = int(math.ceil(tmp_nb_picto / (self.page_row * self.page_col)))
        self.nb_picto = tmp_nb_picto + nb_pages
        if(self.nb_picto <= self.page_row * self.page_col):
            nb_pages = 0
        else:
            nb_pages = int(math.ceil(self.nb_picto / (self.page_row * self.page_col)))
        self.nb_picto = tmp_nb_picto + nb_pages
        nb_pages = int(math.ceil(self.nb_picto / (self.page_row * self.page_col))) - 1
        page_size = self.page_row * self.page_col

        #Root page of the grid (first page)
        current_name = self.root_name
        current_page = Page(current_name,self.page_row,self.page_col)
        self.pages.update({current_name : current_page})

        #Creation of the page tree with the root page
        self.page_tree = PageTreeNode(self.root_name)
        parent = self.page_tree

        #Queue for BFS
        node_queues = []

        #Page counter
        page_counter = 0

        #Creation of the tree
        for i in range(nb_pages):
            
            #New directory pictogram
            new_name = "default"+str(i)

            #New page in the grid
            self.pages.update({new_name : Page(new_name,self.page_row,self.page_col)})

            #Append the node in the tree
            new_node = PageTreeNode(new_name)

            #If the current page is full, create a new one
            if(page_counter >= page_size):
                #Change the current page (children of the parent)
                if(node_queues):

                    #Find the next node that will be the new page to fill with directories
                    next_node = node_queues.pop(0)
                    #Get the new page as the current
                    current_page = self.pages[next_node.page]
                    #The parent becomes the current node
                    parent = next_node
                
                page_counter = 0
            
            #Add the directory pictogram responsible of the new page
            current_page.add_word_to_pictogram(new_name,is_directory = True,warnings = self.warnings)
            self.picto_voc.update({new_name : [parent]})
            page_counter += 1

            #Insert the node and append it to the queue
            parent.insert_child(new_node)
            node_queues.append(new_node)

            #Update the parent pictogram for the link between pages
            self.pages[new_name].parent_picto = self.pages[parent.page].pictograms[new_name]

    def generate_grid_from_txt(self,corpus):
        '''Generate a grid from a .txt corpus

        :param corpus: source text file list containing the corpus
        :type corpus: `.txt` file list
        '''

        #Get the vocabulary of the corpus and the number of pictograms
        voc = get_vocabulary_from_corpus(corpus)

        self.generate_grid_structure(voc)

        page_queue = []
        
        for page in self.pages.values():
            if(len(page.pictograms) < self.page_row * self.page_col):
                page_queue.append(page)

        current_page = page_queue.pop(0)
        
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
            ret_full = current_page.add_word_to_pictogram(word,warnings = self.warnings)
            
            #If the current page is full, the pictogram was not added, create a new page
            if(ret_full == True):

                #New page
                if(page_queue):
                    current_page = page_queue.pop(0)

                #Add the pictogram to the new page
                current_page.add_word_to_pictogram(word,warnings = self.warnings)

            if(word in self.picto_voc):
                self.picto_voc[word].append(self.page_tree.find_node(current_page.name))
            else:
                self.picto_voc.update({word : [self.page_tree.find_node(current_page.name)]})
    
    def swap_pictograms(self,picto_a,picto_b):
        '''Method to swap two pictograms in the whole grid'''

        #---CONDITION BEFORE THE SWAP---#

        page_a = self.pages[picto_a.page_name]
        page_b = self.pages[picto_b.page_name]

        #If there is already the word in the page, do no process the swap
        if(picto_a.word in page_b.pictograms or picto_b.word in page_a.pictograms):
            return

        #---NODES INFORMATION---

        #print(picto_a,"<-->",picto_b)

        #Find the page node corresponding to the page of the pictogram a
        node_a = self.page_tree.find_node(picto_a.page_name)

        #Find the page node corresponding to the page of the pictogram b
        node_b = self.page_tree.find_node(picto_b.page_name)

        #Modify the information of page nodes for the pictogram a
        self.picto_voc[picto_a.word].remove(node_a)
        self.picto_voc[picto_a.word].append(node_b)

        #Modify the information of page nodes for the pictogram b
        self.picto_voc[picto_b.word].remove(node_b)
        self.picto_voc[picto_b.word].append(node_a)

        #---PAGES AND PICTOGRAM INFORMATION---
        
        #Build new pictograms
        new_id_a = str(picto_a.word+"@"+picto_b.page_name)
        new_id_b = str(picto_b.word+"@"+picto_a.page_name)
        new_picto_a = Pictogram(picto_a.word,picto_b.row,picto_b.col,picto_b.page_name,new_id_a,picto_a.is_directory)
        new_picto_b = Pictogram(picto_b.word,picto_a.row,picto_a.col,picto_a.page_name,new_id_b,picto_b.is_directory)

        #Swap
        self.pages[picto_a.page_name].pictograms.pop(picto_a.word)
        self.pages[picto_b.page_name].pictograms.pop(picto_b.word)

        self.pages[picto_a.page_name].pictograms.update({new_picto_b.word : new_picto_b})
        self.pages[picto_b.page_name].pictograms.update({new_picto_a.word : new_picto_a})


  #=========================================================================================================================

  # PRINT AND DISPLAY METHODS OF THE GRID
  #--------------------------------------------------------------

    def to_csv(self,output_file = "default.csv"):
        '''Method to transform the grid into a csv file'''

        #Opening the csv file
        f = open(output_file,"w",encoding = "utf-8",newline = '')

        #Initialization of the writer
        writer = csv.writer(f)
        
        #Get the vocabulary (the grid)
        header = [self.root_name,self.page_row,self.page_col]
        writer.writerow(header)
        header = ['word','row','col','page','identifier','is_dir','link']
        writer.writerow(header)
        
        for page in self.pages.values():

            for picto in page.pictograms.values():

                new_line = picto.in_list()
                writer.writerow(new_line)

        f.close()

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