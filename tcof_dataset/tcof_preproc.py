import codecs
#XML or TRS file
import xml.etree.ElementTree as ET
import sys

#Spacy
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop

#Json
import json

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
    
def tcof_preprocessing(input_file,output_file = "output.txt",stop_words = True):
    '''Function to clean a file coming from the tcof dataset.'''

    #Load the fr model (lemmatizer, morpholizer, parser, tok2vec, ...)
    nlp = spacy.load('fr_core_news_md')

    #Load the stopwords list from the spacy library
    stopwords = tcof_stopwords_load("../../tcof_stopwords.json")

    #Loading the input file
    input_f = open(input_file).read()

    #Output file initialization
    output_f = codecs.open(output_file,"w","utf-8")

    #Processing pipeline
    doc = nlp(input_f)
    
    for token in doc:
    
        if(token.lemma_ not in stopwords or stop_words == False):
            new_token = token.lemma_.lower()
            #Strip the start of the word in the tcof
            new_token = new_token.strip('-')

            if(token.lemma_.endswith('\n')):
                #Write and strip the hesitation in the tcof
                output_f.write(str(new_token.strip("/")))
            else:
                output_f.write(str(new_token.strip("/")) + " ")

    output_f.close()

if __name__ == "__main__":

    #Get the arguments from the console
    args = sys.argv

    #--PIPELINE--

    #From raw trs to raw txt
    trs_to_txt(args[1],args[2])

    #From raw txt to preprocessed txt
    tcof_preprocessing(args[2],args[3])