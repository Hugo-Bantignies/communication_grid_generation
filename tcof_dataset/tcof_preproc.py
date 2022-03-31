from cgitb import text
import sys
import os
from tqdm import tqdm

import codecs
#XML or TRS file
import xml.etree.ElementTree as ET

#Spacy
import spacy
#from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop

#Stanza
import stanza
import spacy_stanza

#Json
import json

#Regular expression
import re

#dbnary_export
from dbnary_export import *



def trs_to_txt(input_path,output_path = "default.txt"):
    '''Function to convert a ".trs" file into a ".txt" file'''

    if(input_path.endswith('.trs')):
        #Open the output file
        output_file = codecs.open(output_path,"w","utf-8")

        #Get the XML tree
        tree = ET.parse(input_path)
        root = tree.getroot()

        data = []

        #Get the text from each element of the tree
        for node in root.findall('.//Turn'):
            tmp = []
            for text in node.itertext():
                if(text.strip()):
                    tmp.append(text.strip())
            data.append(tmp)
        
        #Write in a txt file the text
        for d in data:
            for elem in d:
                output_file.write(str(elem) + " ")
            output_file.write(str("\n"))

        #Close the file
        output_file.close()

def tcof_stopwords_write(input_file = "default.json",stopwords = []):
    '''Function to write a stopwords list into a JSON file.
    '''

    #Write the list in the JSON file
    with codecs.open(input_file,'w',"utf-8") as file:
        json.dump(stopwords,file,indent=0)
    
    file.close()
    
def tcof_stopwords_load(input_file):
    '''Function to load a stopwords list from a JSON file.
    '''

    if(input_file.endswith(".json")):
        #Extract the list from the JSON file
        with codecs.open(input_file,"r","utf-8") as file:
            stopwords = json.load(file)
        
        file.close()

        return stopwords
        
    
    else:
        raise Exception("Not correct file format, .json was expected !")
    
def check_trancript_symbol(word):
    '''Function to filter transcript sumboles from the TCOF dataset
    '''

    #Left hesitation, right hesitation, start of the word
    res = (re.search("^/.+",word) or re.search(".+/$",word) or re.search(".+-$",word) 
            or re.search("^-.+",word) or re.search(".*=.*",word) or re.search(".*\(.*",word) or re.search(".*\).*",word))
    if res:
        return True

    else:
        return False
    
def tcof_preprocessing(input_file,nlp,dico,output_file = "output.txt",stop_words = True):
    '''Function to clean a file coming from the tcof dataset.'''

    #Load the stopwords list from the spacy library
    stopwords = tcof_stopwords_load("tcof_stopwords.json")

    #Loading the input file
    input_f = open(input_file).read()

    #Output file initialization
    output_f = codecs.open(output_file,"w","utf-8")

    #Processing pipeline
    doc = nlp(input_f)

    #For each sentence in the result
    for sent in doc.sents:

        new_sent = ""
    
        #For each token in the sentence
        for token in sent:
        
            #If not a stopword or not a transcript symbol
            if((token.lemma_ not in stopwords or stop_words == False) and (check_trancript_symbol(token.lemma_) == False)):
                
                new_token = token.lemma_.lower()
                new_token = new_token.strip("?")

                if(dico.get(new_token) is not None):
                    if(new_sent == ""):
                        new_sent = new_token
                    else:
                        new_sent = new_sent + " " + new_token

        #Write the sentence in the file
        output_f.write(str(new_sent) + "\n")

    output_f.close()


def tcof_pipeline(directory_path):

    #Load the fr model (lemmatizer, morpholizer, parser, tok2vec, ...)
    nlp = spacy_stanza.load_pipeline("fr",verbose = False,use_gpu = False)

    #Loading the dictionary
    dico = load_dictionary("../../french.json")

    #Get all the files in the directory
    name_list = []
    for root, dirs, files in os.walk(directory_path+"/transcripts_trs"):
        for name in files:
            name_list.append(name)
    
    nb_file = len(name_list)
    for i in tqdm(range(nb_file), desc = "Preprocessing", unit = "file"):
        file_start = name_list[i].strip(".trs")

        #--PIPELINE--

        #From raw trs to raw txt
        trs_to_txt(directory_path+"/transcripts_trs/"+name_list[i],directory_path+"/transcripts_txt/"+file_start+".txt")

        #From raw txt to preprocessed txt
        tcof_preprocessing(directory_path+"/transcripts_txt/"+file_start+".txt",nlp,dico,directory_path+"/preproc_transcripts_txt/"+file_start+".txt")

tcof_pipeline("Corpus_test")