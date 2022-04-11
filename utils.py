import math
import numpy as np
import pandas as pd
import codecs

def dot_product(v_a,v_b):
    '''Function to compute the dot product between two vectors'''
    
    dot_product = 0

    for i in range(len(v_a)):   
        dot_product = dot_product + v_a[i] * v_b[i]
    
    return dot_product

def magnitude(v_a):
    '''Function to compute the magnitude/norm of a vector'''

    vector_sum = 0

    for i in range(len(v_a)):
        vector_sum = vector_sum + v_a[i] * v_a[i]
    
    return math.sqrt(vector_sum)


def cosine_similarity(v_a,v_b):
    '''Function to compute the cosine_similarity of two vectors'''

    return dot_product(v_a,v_b) / (magnitude(v_a) * magnitude(v_b))

def get_vocabulary_from_csv(input_file, separator = ","):
    '''Function that will find the whole vocabulary from the input csv file
    
    :param input_file: csv file containing a pictogram grid
    :type input_file: 'csv' file
    '''

    #Initialization of the vocabulary to return
    voc = dict()
    
    #Read the input csv/tsv file
    df = pd.read_csv(input_file,sep = separator)

    size = df["word"].size

    words = df["word"]
    rows = df["row"]
    cols = df["col"]
    pages = df["page"]
    identifiers = df["identifier"]
    
    #For each word, build the pictogram and add it
    for i in range(size):
        voc[identifiers[i]] = [words[i],rows[i],cols[i],pages[i],identifiers[i]]
    
    return voc

def get_vocabulary_from_corpus(corpus):
    '''Function that will find the whole vocabulary from the input corpus
    
    :param corpus: Corpus containing multiple '.txt' files.
    :type corpus: list of 'txt' files.
    '''

    #Initialization of the vocabulary to return
    voc = []

    for file_path in corpus:
        #Read the input txt file
        with codecs.open(file_path,"r","utf_8") as rawFile:

            #For each line in the file, split the line
            for line in rawFile:
                sentence = line.strip()
                sentence = sentence.lower()
                splittedLine = sentence.split(" ")

                #For each word in the splitted line, store it in the vocabulary of the corpus
                for word in splittedLine:
                    if(word not in voc):
                        voc.append(word)
        rawFile.close()

    return voc