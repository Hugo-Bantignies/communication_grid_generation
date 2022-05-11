from PictogramGrid import Pictogram,Page,Grid
from EvaluationGrid import grid_distance_cost,sentence_distance_cost
from gpgo import gpgo
import os
import random

def mutation_inter(ind):

      #Random selection of the two pages
      selected_page_a = random.choice(list(ind.pages))
      page_a = ind.pages[selected_page_a]

      selected_page_b = random.choice(list(ind.pages))
      page_b = ind.pages[selected_page_b]

      #Selection of the two pictograms to swap
      if(page_a.pictograms != dict()):
        selected_picto_a = page_a.pictograms[random.choice(list(page_a.pictograms))]

      if(page_b.pictograms != dict()):
        selected_picto_b = page_b.pictograms[random.choice(list(page_b.pictograms))]
    
      #If both pictograms are not directory or not the same, we perform the swap
      if(selected_picto_a.is_directory == False and selected_picto_b.is_directory == False 
                and selected_picto_a.word != selected_picto_b.word):

        ind.swap_pictograms(selected_picto_a,selected_picto_b)

      return ind

def mutation(ind):
    #Random selection of a page
    selected_page_name = random.choice(list(ind.pages))
    selected_page = ind.pages[selected_page_name]

    #Random selection of the pictogram to ducplicate
    if(selected_page.pictograms != dict()):
        sel_pic = selected_page.pictograms[random.choice(list(selected_page.pictograms))]

    selected_page = None

    #Selection of a page having an empty space
    for page in ind.pages.values():
        if(page.is_full == False):
          selected_page = page
          break

    #Adding the duplicata
    if(selected_page != None and sel_pic.is_directory == False and sel_pic.word not in selected_page.pictograms):

        #Adding in the page
        ret = selected_page.add_word_to_pictogram(sel_pic.word,sel_pic.is_directory,warnings = True)
        #Adding in the vocabulary
        if(ret == False):
            ind.picto_voc[sel_pic.word].append(ind.page_tree.find_node(selected_page.name))
    
        print("DUPLICATA :",sel_pic.word,selected_page.name)

corpus = []
input_grid_file = "default.csv"

for root, dirs, files in os.walk("training_corpora"):
    for name in files:
        corpus.append(os.path.join(root,name))

g = Grid(corpus,randomizer=False,warnings=False)

mf = dict()


for i in range(100):
    mutation_inter(g)
    mutation(g)
    sentence_distance_cost(g,"le chat est petit oiseaux dauphin mer eau mulot serpent".split(" "))
g.to_csv()

g.display_information()
