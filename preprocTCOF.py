#Spacy
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop

#Nltk
import nltk

#Other
import codecs

def tcof_preprocessing(input_file,output_file = "output.txt",stop_words = True):

    #Load the fr model (lemmatizer, morpholizer, parser, tok2vec, ...)
    nlp = spacy.load('fr_core_news_md')

    #Load the stopwords list from the spacy library
    stopwords = list(fr_stop)

    #Loading the input file
    input_f = open(input_file).read()

    #Output file initialization
    output_f = codecs.open(output_file,"w","utf-8")

    #Processing pipeline
    doc = nlp(input_f)
    
    for token in doc:
        if(token.lemma_ not in stopwords or stop_words == False):
            if(token.lemma_.endswith('\n')):
                output_f.write(str(token.lemma_.lower()))
            else:
                output_f.write(str(token.lemma_.lower()) + " ")

    output_f.close()



tcof_preprocessing(input_file = "lilou1_hua.txt",output_file = "lilou1_hua_lemm.txt")