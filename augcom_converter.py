import csv
import json
import codecs
import string

def get_pagelist(input_file):

    if(input_file.endswith(".json")):

        #Extract the list from the JSON file
        with codecs.open(input_file,"r","utf-8") as file:
            dico = json.load(file)

        pages = dict()
        root_page = None

        for p in dico["PageList"]:

            if(root_page == None):
                root_page = p['Name']

            pages.update({p['Name'] : p['ElementIDsList']})

        file.close()

        return pages,root_page

def elements(input_file):

    if(input_file.endswith(".json")):

        #Extract the list from the JSON file
        with codecs.open(input_file,"r","utf-8") as file:
            dico = json.load(file)

        elements = dict()

        page_order = []

        for el in dico["ElementList"]:
            if("x" not in el or "y" not in el):
                pass
            else:
                type = el["Type"]
                if(el["Type"] != "button"):
                    type = el["Type"]["GoTo"]
                    if(type not in page_order):
                        page_order.append(type.upper())

                elements.update({el["ID"] : [el["x"],el["y"],type,el["ID"]]})
     
    return elements,page_order

def augcom_to_csv(input_file,output_file = "default.csv"):

    #Opening the csv file
    f = open(output_file,"w",encoding = "utf-8",newline = '')

    #Initialization of the writer
    writer = csv.writer(f)

    elems,page_order = elements(input_file)
    pages,root_page= get_pagelist(input_file)

    page_order = [root_page] + page_order

    #Header
    header = ['word','row','col','page','identifier','is_dir','link','sim_score',root_page,3,5]
    writer.writerow(header)


    elems_queue = []

    for p in page_order:
        if(p == "#HOME" or p == "Accueil"):
            page_name = "Accueil"
        else:
            page_name = p.upper()

        for el in pages[page_name]:
            if(el in elems):
                elems_queue.append(elems[el] + [page_name])

    visited_links = []

    #Insert each elements
    for el in elems_queue:
        page = el[4]
        id = str(el[3]) + "@" + str(page)

        link = None
        
        if(el[2] == "button"):
            dir = "NO"
        else:
            dir = "DIR"
            link = el[2].upper()

        if(link not in visited_links and link != None):

            new_line = [link,el[0],el[1],page,id,dir,link,0]
            visited_links.append(link)
            writer.writerow(new_line)

        elif(link == None):
            new_line = [el[3].rstrip(string.digits),el[0],el[1],page,id,dir,link,0]
            writer.writerow(new_line)
    
    f.close()


augcom_to_csv("../podd.augcom/podd.json","podd.csv")