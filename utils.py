import pandas as pd
import codecs
#XML or TRS file
import xml.etree.ElementTree as ET

def csv_to_txt(file_path, output_path = "input_corpora/default.txt",separator = "\t",row_number = -1):

    #Initialization of the vocabulary to return
    voc = []

    #Open the output file
    output = codecs.open(output_path,"w","utf-8")
    
    #Read the input csv/tsv file
    df = pd.read_csv(file_path,sep = separator)

    #Get the sentence column
    sentences = df['sentence']
    if(row_number == -1):
        size = len(sentences)
    else:
        size = min(len(sentences),row_number)
    
    #For each sentence, split the sentence and add each word to the vocabulary
    for i in range(size):
        sentence = sentences[i]
        sentence = sentence.strip()
        sentence = sentence.lower()
        if(i != size - 1):
            output.write(str(sentence)+"\n")
        else:
            output.write(str(sentence))
    
    #Close the output file
    output.close()


def trs_to_txt(input_path,output_path = "default.txt"):
    '''Function to convert a ".trs" file into a ".txt" file'''

    #Open the output file
    output_file = codecs.open(output_path,"w","utf-8")

    #Get the XML tree
    tree = ET.parse(input_path)
    root = tree.getroot()

    #Get the text from each element of the tree
    data = [text.strip() for node in root.findall('.//Turn') for text in node.itertext() if text.strip()]
    
    #Write in a txt file the text
    for d in data:
        output_file.write(str(d) + "\n")

    #Close the file
    output_file.close()
    

def get_vocabulary_from_txt(file_path):

    #Initialization of the vocabulary to return
    voc = []

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

    return voc