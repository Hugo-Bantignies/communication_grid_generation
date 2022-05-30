import random
from PictogramGrid import Grid
from EvaluationGrid import *
from utils import *

from os.path import exists
from tqdm import tqdm
import yaml

#Paralellization
import multiprocessing as mp

#DEAP Framework (Genetic Algorithm)
from deap import base
from deap import creator
from deap import tools

#fastText
import fasttext
import fasttext.util


class gpgo():
    '''Object that will compute an optimized grid from an initial grid using 
       an Evolutionary Algorithm (Genetic Algorithm) for a Pictogram Grid Communication System (PGCS)

    :source_files: source_files name or corpus from the one the optimizer will generate an optimal grid (`.txt`,`.csv`, Augcom)
    :type source_files: string
    :evaluation_files: training file name to train the optimization of the grid.
    :type source_files: string
    :pop_size: size of the initial population, optional (10 by default)
    :type pop_size: integer
    :cross_proba: probability of having a crossover between two individuals, optional (0.5 by default)
    :type cross_proba: float ([0,1])
    :cross_info_rate: rate of information the selected individual will provide to the child after a crossover, optional (0.5 by default)
    :type cross_info_rate: float ([0,1])
    :mutation_proba: probability of having a mutation for one individual, optional (0.5 by default)
    :type mutation_proba: float ([0,1])
    :select_number: number of individual to select during the selection, optional (2 by default)
    :type select_number: integer
    :gen_number: number of generation the optimizer will process, optional (10 by default)
    :type gen_number: integer
    :randomizer: if True, the initial population of the grid will contain random grids, else the grids will follow the source_files, optional (True by default)
    :type gen_number: boolean
    :similarity_coefficient: coefficient corresponding of the proportion of the type of display of the grid
    :type similarity_coefficient: float ([0,1])
    :sim_model: Language model to compute the similarity between words (Word2Vec, Glove, ...)
    :type sim_model: model
    '''
    
    def __init__(self, source_files, evaluation_files, pop_size = 10, cross_proba = 0.5, cross_info_rate = 0.5,
                 mutation_proba = 0.5, select_number = 2, gen_number = 10, randomizer = True, page_row_size = 5, 
                 page_col_size = 5, similarity_coefficient = 0.5, sim_model_path = None, sim_matrix_path = "sim_default.json"):
                 
        '''Constructor
        '''

        self.source_files = source_files
        
        #The evaluation file has to be a .txt file.
        if(evaluation_files[0].endswith('.txt')):
            self.evaluation_files = evaluation_files

        #File format not accepted
        else:
            raise Exception("Not accepted evaluation file format !")

        self.pop_size = pop_size

        #Check the cross probability is between 0 and 1
        if(cross_proba < 0 or cross_proba > 1):
            raise Exception("Unexpected crossover probability (not between 0 and 1) !")
        self.cross_proba = cross_proba

        #Check the cross rate is between 0 and 1
        if(cross_info_rate < 0 or cross_info_rate > 1):
            raise Exception("Unexpected crossover information rate (not between 0 and 1) !") 
        self.cross_info_rate = cross_info_rate

        #Check the mutation probability is between 0 and 1
        if(mutation_proba < 0 or mutation_proba > 1):
            raise Exception("Unexpected mutation probability (not between 0 and 1) !") 

        self.mutation_proba = mutation_proba

        self.select_number = select_number

        self.gen_number = gen_number

        self.randomizer = randomizer

        self.page_row = page_row_size
        self.page_col = page_col_size

        #Check the similarity coefficient
        if(similarity_coefficient < 0 or similarity_coefficient > 1):
            raise Exception("Unexpected similarity coefficient (not between 0 and 1) !") 

        if(sim_model_path == None):
          self.similarity_coefficient = 0
        else:
          self.similarity_coefficient = similarity_coefficient

        self.fitness_log = dict()

        self.best_history = []

        #Genetic objects initialization
        self.toolbox = base.Toolbox()
        self.init_genetic_objects()

        #Genetic operations initialization
        self.init_operations()

        self.sim_matrix = None
        self.sim_model_path = sim_model_path
        self.sim_matrix_path = sim_matrix_path

        #Similarity matrix loading
        if(self.similarity_coefficient > 0):
          #Precomputing of the similarity matrix or loading from a JSON if the path exists
          if(not exists(sim_matrix_path)):
            tmp_voc  = get_vocabulary_from_corpus(self.source_files)

            #Load similarity model
            self.sim_model = fasttext.load_model(self.sim_model_path)

            #Compute the similarity matrix
            self.sim_matrix = compute_word_similarities(tmp_voc,self.sim_model)
            store_similarity_matrix(self.sim_matrix,output_file = self.sim_matrix_path)
            
          else:
            self.sim_matrix = load_similarity_matrix(self.sim_matrix_path)

    def fitness_history_record(self,fitnesses,gen_idx):
      '''Update the fitness history with a new fitness record and the corresponding generation as key
      
      :param fitnesses: Value added to the history. List containing the fitnesses of the new individuals of the generation (new fitnesses) 
      :type fitnesses: list
      :param gen_idx: Key added to the history. Number of the corresponding generation
      :type gen_idx: integer
      '''

      self.fitness_log.update({gen_idx:fitnesses})

    def fitness_best_record(self,fitness):
      '''Update the best fitness history with the record of the best fitness ever. 
      
      :param fitness: Value added to the history. List containing the fitnesses of the new individuals of the generation (new fitnesses) 
      :type fitness: float
      '''

      self.best_history.append(fitness)

    def init_individual(self,container,source_files):
      '''Method to initialize one individual (Grid) for the Optimizer
      
      :param container: Encapsulation structure for the Grid.
      :type container: container
      :param source_files: Vocabulary or file from which the grid will be generated.
      :type source_files: file or Dict
      :return: returns a container
      :rtype container: container
      '''
      #Create an encapsulated grid in the container to fit with the DEAP framework (from the source file)
      return container(source_files,root_name = "accueil",randomizer = self.randomizer,warnings = False,
                       page_row_size = self.page_row,page_col_size = self.page_col)

    def init_population(self,container,func,source_files):
      '''Method to initialize the population of the Optimizer
      
      :param container: Encapsulation structure for the population.
      :type container: container
      :param source_files: Vocabulary or file from which the grid will be generated.
      :type source_files: file or Dict
      :return: returns a container
      :rtype container: container
      '''

      #Create a population of individuals. The size of the population is the initial population size. 
      return container(func(source_files) for i in range(self.pop_size))


    def init_genetic_objects(self):
      '''Method that will initialize the objects for the genetic algorithm
      '''

      #Creator for the fitness and the individual types
      creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
      creator.create("Individual", Grid, fitness=creator.FitnessMin)
        
      #Individual definition
      self.toolbox.register("individual", self.init_individual, creator.Individual)

      #Population definition (using initRepeat, we will generate a list of individual)
      self.toolbox.register("population", self.init_population, list, self.toolbox.individual)

    def production_cost(self,individual):
      '''Method used by the optimizer to evaluate one individual by using the production cost

      :param individual: The inidividual the optimizer will evaluate
      :type individual: individual
      :return: returns the production cost of the grid
      :rtype: (float,)
      '''
      return grid_cost(individual, self.evaluation_files,sim_matrix = self.sim_matrix, similarity_coefficient=self.similarity_coefficient),

    def crossover_picto_inter(self,ind_x, ind_y):
      '''Method used by the optimizer to perform a crossover between two individuals and generate a new one

      :param ind_x: The first individual for the crossover (parent x)
      :type ind_x: individual
      :param ind_y: The second individual for the crossover (parent y)
      :type ind_y: individual
      :return: returns the childs of the two parents (crossover result)
      :rtype: individual,individual
      '''

      for i in range(math.ceil(ind_x.nb_picto * self.cross_info_rate)):
        #Get the pictogram of the individual y
        page_y = random.choice(list(ind_y.pages.values()))
        picto_y = random.choice(list(page_y.pictograms.values()))

        if(picto_y.is_directory == False):

          #Get the pictogram of the word of the picto_y in the individual x
          page_name_x = random.choice(ind_x.picto_voc[picto_y.word]).page
                  
          picto_target_x = ind_x.pages[page_name_x].pictograms[picto_y.word]

          #Find the pictogram having the same position of the previous one
          picto_to_swap_x = None

          for picto_x in ind_x.pages[page_y.name].pictograms.values():

            if(picto_x.is_directory == False and picto_x.row == picto_y.row and picto_x.col == picto_y.col):

              picto_to_swap_x = picto_x

          #Do not swap the same pictogram
          if(picto_to_swap_x and picto_target_x.word != picto_to_swap_x.word):
            ind_x.swap_pictograms(picto_target_x,picto_to_swap_x)

      return ind_x,ind_x

    def mutation_swap_picto_intra(self,ind):
      '''Method used by the optimizer to perform a mutation on one individual
      The mutation will perform a random swap (intra) of two pictograms within the same page.

      :param ind: the individual subject to the mutation
      :type ind: individual
      :return: returns the individual after the mutation
      :rtype: individual
      '''

      #Random selection of a page
      selected_page_name = random.choice(list(ind.pages))
      selected_page = ind.pages[selected_page_name]

      #Random selection of two pictograms within the selected page
      if(selected_page.pictograms != dict()):
        selected_picto_a = selected_page.pictograms[random.choice(list(selected_page.pictograms))]
        selected_picto_b = selected_page.pictograms[random.choice(list(selected_page.pictograms))]

        #Swap the two pictograms
        selected_page.swap_pictograms(selected_picto_a,selected_picto_b)

      return ind

    def mutation_swap_picto_inter(self,ind):
      '''Method used by the optimizer to perform a mutation on one individual
      The mutation will perform a random swap (inter) of two pictograms in different page.

      :param ind: the individual subject to the mutation
      :type ind: individual
      :return: returns the individual after the mutation
      :rtype: individual
      '''

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
      if(selected_picto_a.word != selected_picto_b.word):

        ind.swap_pictograms(selected_picto_a,selected_picto_b)

      return ind
      
    def mutation_duplicata(self,ind):
      '''Method used by the optimizer to perform a mutation on one individual
      The mutation will perform a duplicata of a random pictogram within the grid.

      :param ind: the individual subject to the mutation
      :type ind: individual
      :return: returns the individual after the mutation
      :rtype: individual
      '''

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
        selected_page.add_word_to_pictogram(sel_pic.word,sel_pic.is_directory,warnings = False)
        ind.picto_voc[sel_pic.word].append(ind.page_tree.find_node(selected_page.name))

      return ind

    def mutation_exportation(self,ind):
      '''Method used by the optimizer to perform a mutation on one individual
      The mutation will perform an exportation of a random pictogram within the grid.

      :param ind: the individual subject to the mutation
      :type ind: individual
      :return: returns the individual after the mutation
      :rtype: individual
      '''

      #Random selection of a page
      selected_page_name = random.choice(list(ind.pages))
      selected_page = ind.pages[selected_page_name]

      #Random selection of the pictogram to export
      if(selected_page.pictograms != dict()):
        sel_pic = selected_page.pictograms[random.choice(list(selected_page.pictograms))]

      target_page = None

      #Selection of a page having an empty space
      for page in ind.pages.values():
        if(page.is_full == False):
          target_page = page
          break
      
      #Adding the exported pictogram
      if(target_page != None and sel_pic.is_directory == False and sel_pic.word not in target_page.pictograms):

        #Adding in the page
        target_page.add_word_to_pictogram(sel_pic.word,sel_pic.is_directory,warnings = False)
        ind.picto_voc[sel_pic.word].append(ind.page_tree.find_node(target_page.name))

        #Removing the pictogram
        selected_page.remove_word_to_pictogram(sel_pic.word)
        ind.picto_voc[sel_pic.word].remove(ind.page_tree.find_node(selected_page.name))

      return ind

    def mutation_picto(self,ind):

      r = random.randint(1,4)
      
      if(r == 1):
        #Mutation Duplicata
        ind = self.mutation_duplicata(ind)
      
      elif(r == 2):
        #Mutation Exportation
        ind = self.mutation_exportation(ind)

      elif(r == 3):
        #Mutation Swap Inter Picto
        ind = self.mutation_swap_picto_intra(ind)

      else:
        #Mutation Swap Intra Picto
        ind = self.mutation_swap_picto_inter(ind)

      return ind



    def init_operations(self):
      '''Method that will initialize operations used by the genetic algorithm (evaluation, selection, crossover, mutation)
      '''

      #--Evaluation definition--
      self.toolbox.register("evaluation", self.production_cost)

      #--Selection definition--

      #Using tools.selBest (select the k best individuals following the fitness)
      self.toolbox.register("selection", tools.selBest) 

      #--Crossover definition--
      self.toolbox.register("crossover",self.crossover_picto_inter)

      #--Mutation definition--
      self.toolbox.register("mutation",self.mutation_picto)
  

    def genetic_algorithm(self,pid = 0):
      '''Method that will use a genetic algorithm to generate an optimal grid starting from a random generation.

      :param pid: Process id
      :type: integer
      :return: Returns the best individual of the last generation (optimized grid)
      :rtype: class: Grid
      '''

      #====INITIAL GENERATION====

      #Initialization of the population
      pop = self.toolbox.population(self.source_files)

      #Initialization of the best individual
      best_ind = pop[0]
      best_gen = 0

      #Evaluation of the initial population

      fitnesses = list(map(self.toolbox.evaluation,pop))
      min_init_fit = math.inf,

      #Recording fitnesses
      self.fitness_history_record(fitnesses,0)

      #For each individual in the population, associate the fitness to the individual
      for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

        #Keep the best individual of the initial population
        if(fit < min_init_fit):
          min_init_fit = fit
          best_ind = ind

      #Record of the best fitness
      self.fitness_best_record(best_ind.fitness.values[0])

      #print("DEBUG : INITIAL GENERATION (0) --> Best fitness : " + str(best_ind.fitness.values[0]) + "\n")

      #==ITERATION OVER GENERATIONS==

      #Iterative process : For each generation
      for gen in tqdm(range(1,self.gen_number+1),desc = "Process : "+str(pid),unit = "generation",position = pid):

        #--SELECTION--

        #Select the k best individuals of the current generation
        offspring = self.toolbox.selection(pop,self.select_number)
        # Clone the selected individuals
        offspring = list(map(self.toolbox.clone, offspring))

        #--CROSSOVER--
        for ind1,ind2 in zip(offspring[::2], offspring[1::2]):

          #Probability to perform the crossover
          if(random.random() < self.cross_proba):
            
            #Crossover operation to generate the new individual
            new_ind1,new_ind2 = self.toolbox.crossover(ind2,ind1)
            offspring.append(new_ind1)
            offspring.append(new_ind2)

        #--MUTATION--
        for ind in offspring:

          #Probability to perform a mutation
          if(random.random() < self.mutation_proba):

            #Mutation operation to modify the individual
            offspring.remove(ind)
            mutant = self.toolbox.mutation(ind)
            del mutant.fitness.values
            offspring.append(self.toolbox.clone(mutant))

        #--EVALUATION--

        #Avoid useless computation
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

        #Evaluation of the population
        fitnesses = list(map(self.toolbox.evaluation,invalid_ind))
          
        #Recording fitnesses
        self.fitness_history_record(fitnesses,gen)

        #For each new individual in the population, associate the fitness to the individual
        for ind, fit in zip(invalid_ind, fitnesses):
          ind.fitness.values = fit

        #--NEW GENERATION--
        pop[:] = offspring

        #Save the best individual of the population
        for ind in pop:
          if(ind.fitness.values < best_ind.fitness.values):
            best_ind = ind
            best_gen = gen

        #Record of the best fitness
        self.fitness_best_record(best_ind.fitness.values[0])
        
      #Final best grid
      best_fitness = self.toolbox.evaluation(best_ind)[0]
      #print("DEBUG : Best individual --> Generation : " + str(best_gen) + ", Fitness : " + str(best_fitness))
      return best_ind,best_fitness

    #===============================================
    # DISPLAY METHODS AND HISTORY
    #===============================================

    def fitness_history(self,option = "only_best"):
      '''Methods returning the fitness history depending on the request from the user (parameters) for each process.

      :param option: Option to know what the history will contain, optional ("best" by default)
      Possible options : "gen_best", "only_best", "average", "all"
      :type: string
      :return: Returns the prepared history depending of the options and the request from the user.
      :rtype: list
      '''

      #Get the best history
      if(option == "only_best"):
        return self.best_history

      #Get the average history
      elif(option == "average"):

        #History
        history = []

        for fitness in self.fitness_log.values():
          #Append the average of the fitness for the generation in the history to return (if the list is not empty)
          if(fitness):
            
            tmp_avg = []

            for value in fitness:

              tmp_avg.append(value[0])
            
            history.append(sum(tmp_avg) / len(tmp_avg))
            
        return history
      
      elif(option == "gen_best"):

        #History
        history = []

        for fitness in self.fitness_log.values():
          #Append the average of the fitness for the generation in the history to return (if the list is not empty)
          if(fitness):
            
            tmp_avg = []
            
            for value in fitness:

              tmp_avg.append(value[0])
            
            history.append(min(tmp_avg))
            
        return history

    def save_config(self,config_file = "default.yaml"):

      params = {"pop_size" : self.pop_size,"select_number" : self.select_number,"gen_number" : self.gen_number,
                    "cross_proba" : self.cross_proba,"cross_info_rate" : self.cross_info_rate,"mutation_proba" : self.mutation_proba,
                    "page_row" : self.page_row,"page_col" : self.page_col,"randomizer" : self.randomizer,
                    "similarity_coefficient" : self.similarity_coefficient,"sim_model_path" : self.sim_model_path,"sim_matrix_path" : self.sim_matrix_path}

      with open(config_file,'w') as file:

        documents = yaml.dump(params, file)


    def display_config(self):
        '''Method to display the configuration of the optimizer
        '''

        #Display informations
        print("####### Genetic Pictogram Grid Communication Optimizer #######\n")
        print("## Optimizer Parameters ##")
        print("========================================================================")
        print("------------------------------------------------------------------------")
        print("  INITIAL POPULATION SIZE : "+ str(self.pop_size)+"\n")
        print("  NUMBER OF GENERATION : "+ str(self.gen_number)+"\n")
        print("  CROSSOVER RATE : "+ str(self.cross_proba * 100)+"%     MUTATION RATE : "+ str(self.mutation_proba * 100)+"%\n")
        print("  CROSSOVER INFORMATION RATE : "+ str(self.cross_info_rate * 100)+"%\n")
        print("  SIMILARITY RATE : "+str(self.similarity_coefficient * 100)+"%\n")
        print("------------------------------------------------------------------------")
        print("========================================================================\n")


def load_gpgo(source_files,evaluation_files,config_file):
  '''Function to create a gpgo with a configuration file'''

  if(config_file.endswith('.yaml')):
        
    with open(config_file,'r') as file:

      docs = yaml.load_all(file, Loader=yaml.FullLoader)

      for doc in docs:
            
        return gpgo(source_files,evaluation_files,doc["pop_size"],doc["cross_proba"],doc["cross_info_rate"],
                    doc["mutation_proba"],doc["select_number"],doc["gen_number"],doc["randomizer"],doc["page_row"],
                    doc["page_col"],doc["similarity_coefficient"],doc["sim_model_path"],doc["sim_matrix_path"])
  else:
    raise Exception("Not accepted configuration file format ! (.yaml)")

  