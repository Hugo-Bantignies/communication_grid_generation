#RDFLIB
from cmath import exp
import rdflib
from rdflib import Graph

#Codecs
import codecs

#JSON
import json


def export_dbnary(dbnary_file,output_file = "default.json",language = "fr"):

    #Parsing of dbnary
    g = Graph()
    g.parse(dbnary_file)

    #Opening the JSON file
    dic_file = codecs.open(output_file,"w","utf-8")

    #Dictionary
    dico = dict()


    q = """SELECT * WHERE {
       ?lexeme a ontolex:LexicalEntry ;
         rdfs:label ?label ;
         ontolex:canonicalForm ?form ;
         lime:language ?lang .

    FILTER(?lang = \""""+language+"""\")
    }
    """

    qres = g.query(q)

    for row in qres:
        word = row.label
        dico.update({word : word})
    
    json.dump(dico,dic_file)

    #Closing the output file
    dic_file.close()


def load_dictionary(input_file):

    if(input_file.endswith(".json")):

        #Extract the list from the JSON file
        with codecs.open(input_file,"r","utf-8") as file:
            dico = json.load(file)
        
        file.close()

        return dico
        
    
    else:
        raise Exception("Not correct file format, .json was expected !")

