#!python -m pip install networkx
#!python -m pip install matplotlib==2.2.3
#!python -m pip install ipywidgets
#!python -m pip install graphviz
#!python -m pip install pandas
#!python -m pip install pudb
#!python -m pip install nbconvert
#!python -m pip install nbconvert -U
#coding=utf-8

import random

class TextGenerator():
    '''Object used to generate random text from a vocabulary in a source_file. 

    :source_file: Source file from which the vocabulary will be extracted and the text will be generated.
    :type: string
    :source_file: Output file that will be the generated file.
    :type: string
    :sentence_number: The number of sentences in the generated text
    :type: integer
    :sentence_length: The length of each sentence in the generated text
    :type: integer
    '''

    def __init__(self, source_file, output_file = "output_text.txt", sentence_number = 1000,sentence_length = 5):
        '''Constructor
        '''

        #The source file has to be a .txt file.
        if(source_file.endswith('.txt')):
            self.__source_file = source_file

        #File format not accepted
        else:
            raise Exception("Not accepted source file format !")

        #The output file has to be a .txt file.
        if(output_file.endswith('.txt')):
            self.__output_file = output_file

        #File format not accepted
        else:
            raise Exception("Not accepted output file format !")

        self.__sentence_number = sentence_number
        self.__sentence_length = sentence_length
        
        self.__vocabulary = self.extract_vocabulary()

    def get_source_file(self):
      '''Getter for the source file
      
      :return: Returns the source file name given as input
      :rtype: string
      '''

      return self.__source_file

    def get_output_file(self):
      '''Getter for the output file
      
      :return: Returns the output file name
      :rtype: string
      '''

      return self.__output_file

    def get_sentence_number(self):
      '''Getter for the sentence number
      
      :return: Returns the sentence number of the generator
      :rtype: integer
      '''

      return self.__sentence_number

    def get_sentence_length(self):
      '''Getter for the sentence length
      
      :return: Returns the sentence length of the generator
      :rtype: integer
      '''

      return self.__sentence_length
    
    def get_vocabulary(self):
      '''Getter for the vocabulary of the generator.
      
      :return: Returns the vocabulary of the generator.
      :rtype: list of string
      '''

      return self.__vocabulary

    
    def extract_vocabulary(self):
      '''Method to get the vocabulary from the source file.
      '''
      #Source file opening
      with open(self.get_source_file(),"r") as rawFile:

        rawVoc = []
        #For each line in the file, split the line
        for line in rawFile:
          sentence = line.strip()
          splittedLine = sentence.split(" ")

          #For each word in the splitted line, store it in the vocabulary of the corpus
          for word in splittedLine:
            if(word not in rawVoc):
              rawVoc.append(word)

      return rawVoc

    def generation(self):
      #Output file opening
      with open(self.get_output_file(),"w") as outputFile:
          
        #Generation of the output file sentences
        for sentence_i in range(self.get_sentence_number()):

            #Generation of one sentence
            for word_i in range(self.get_sentence_length()):
                  
                #Get the index of the next word
                voc = self.get_vocabulary()
                word_idx = random.randint(0,len(voc) - 1)
                outputFile.write(str(voc[word_idx]) + " ")
              
            outputFile.write("\n")

      outputFile.close()
            


    

        
