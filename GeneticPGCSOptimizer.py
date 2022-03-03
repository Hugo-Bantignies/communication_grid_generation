#!python -m pip install networkx
#!python -m pip install matplotlib==2.2.3
#!python -m pip install ipywidgets
#!python -m pip install graphviz
#!python -m pip install pandas
#!python -m pip install pudb
#!python -m pip install nbconvert
#!python -m pip install nbconvert -U
#coding=utf-8


# %matplotlib
from queue import Empty
import random
from mimetypes import init
from typing import final
from communication_grid import Grid
from evaluation_cost import *
from tqdm import tqdm

#DEAP Framework (Genetic Algorithm)
from deap import base
from deap import creator
from deap import tools


class GeneticPGCSOptimizer():
    '''Object that will compute an optimized grid from an initial grid using 
       an Evolutionary Algorithm (Genetic Algorithm) for a Pictogram Grid Communication System (PGCS)

    :source_file: source_file name from the one the optimizer will generate an optimal grid (`.txt`,`.csv`, Augcom)
    :type source_file: string
    :eval_file: evalutation file name to evaluate the generated grids.
    :type source_file: string
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
    :randomizer: if True, the initial population of the grid will contain random grids, else the grids will follow the source_file, optional (True by default)
    :type gen_number: boolean
    :cost_average: if True, the computed cost will be the average of the sum of the costs, 
                   else the computed cost will be the sum of the costs, optional (True by default)
    :type cost_average: boolean
    :distance_formula: formula the optimizer will use to compute the cost, optional ("euclidean" by default)
                       available formulas : "euclidean", "manhattan"
    :type source_file: string
    :fitness_history: save all fitnesses during the genetic algorithm
    :type fitness_history: dict
    '''
    
    def __init__(self, source_file, eval_file, pop_size = 10, cross_proba = 0.5, cross_info_rate = 0.5,
                 mutation_proba = 0.5, select_number = 2, gen_number = 10, randomizer = True, cost_average = True, distance_formula = "euclidean"):
        '''Constructor
        '''

        self.__source_file = source_file
        
        #The evaluation file has to be a .txt file.
        if(eval_file.endswith('.txt')):
            self.__eval_file = eval_file

        #File format not accepted
        else:
            raise Exception("Not accepted evaluation file format !")

        self.__pop_size = pop_size

        #Check the cross probability is between 0 and 1
        if(cross_proba < 0 or cross_proba > 1):
            raise Exception("Unexpected crossover probability (not between 0 and 1) !")
        self.__cross_proba = cross_proba

        #Check the cross rate is between 0 and 1
        if(cross_info_rate < 0 or cross_info_rate > 1):
            raise Exception("Unexpected crossover information rate (not between 0 and 1) !") 
        self.__cross_info_rate = cross_info_rate

        #Check the mutation probability is between 0 and 1
        if(mutation_proba < 0 or mutation_proba > 1):
            raise Exception("Unexpected mutation probability (not between 0 and 1) !") 
        self.__mutation_proba = mutation_proba

        self.__select_number = select_number

        self.__gen_number = gen_number

        self.__randomizer = randomizer

        self.__cost_average = cost_average

        #Check the distance formula the optimizer will use to compute the cost
        if(distance_formula != "euclidean" and distance_formula != "manhattan"):
          raise Exception("Unexpected distance fomula (euclidean or manhattan) !")
        self.__distance_formula = distance_formula
        

        self.__fitness_history = dict()

        self.__best_history = []

        #Genetic objects initialization
        self.__toolbox = base.Toolbox()
        self.init_genetic_objects()

        #Genetic operations initialization
        self.init_operations()
      
        #Display the configuration of the optimizer
        self.display_config()

    def get_source_file(self):
      '''Getter for the source file
      
      :return: Returns the source file name given as input
      :rtype: string
      '''

      return self.__source_file

    def get_eval_file(self):
      '''Getter for the evaluation file
      
      :return: Returns the evaluation file name given as input
      :rtype: string
      '''

      return self.__eval_file

    def get_pop_size(self):
      '''Getter for the size of the initial population
      
      :return: Returns the size of the initial population
      :rtype: integer
      '''

      return self.__pop_size

    def get_cross_proba(self):
      '''Getter for the crossover probability of the optimizer
      
      :return: Returns the crossover probability
      :rtype: float
      '''

      return self.__cross_proba

    def get_cross_info_rate(self):
      '''Getter for the crossover information rate of the optimizer
      
      :return: Returns the crossover information rate
      :rtype: float
      '''

      return self.__cross_info_rate
    
    def get_mutation_proba(self):
      '''Getter for the mutation probability of the optimizer
      
      :return: Returns the mutation probability
      :rtype: float
      '''

      return self.__mutation_proba

    def get_select_number(self):
      '''Getter for the number of individual to select during the selection operation
      
      :return: Returns the selection number.
      :rtype: integer
      '''

      return self.__select_number

    def get_gen_number(self):
      '''Getter for the number of generation the optimizer will process
      
      :return: Returns the number of generations
      :rtype: integer
      '''

      return self.__gen_number

    def get_randomizer(self):
      '''Getter for the randomizer telling if the generation of the initial grids in the initial population has to be random or not
      
      :return: Returns the randomizer
      :rtype: boolean
      '''

      return self.__randomizer

    def get_cost_average(self):
      '''Getter for the cost average indicator of the optimizer
      
      :return: Returns the cost average indicator
      :rtype: boolean
      '''

      return self.__cost_average

    def get_distance_formula(self):
      '''Getter for the distance formula the optimizer will use to compute the cost
      
      :return: Returns the distance formula
      :rtype: string
      '''

      return self.__distance_formula

    def get_fitness_history(self):
      '''Getter for the fitness history
      
      :return: Returns the fitness history
      :rtype: dict
      '''

      return self.__fitness_history

    def get_best_history(self):
      '''Getter for the best fitness history
      
      :return: Returns the best fitness history
      :rtype: list
      '''

      return self.__best_history

    def set_source_file(self,source_file):
      '''Setter for the source file name
      
      :param source_file: New source file name given to the optimizer
      :type source_file: string
      '''

      self.__source_file = source_file

    def set_pop_size(self,pop_size):
      '''Setter for the size of the population
      
      :param pop_size: New population size
      :type pop_size: integer
      '''

      self.__pop_size = pop_size

    def set_cross_proba(self,cross_proba):
      '''Setter for the cross probability
      
      :param cross_proba: New cross probability ([0,1])
      :type cross_proba: float
      '''

      #Check the cross probability is between 0 and 1
      if(cross_proba < 0 or cross_proba > 1):
        raise Exception("Unexpected crossover probability (not between 0 and 1) !")
      self.__cross_proba = cross_proba

    def set_cross_info_rate(self,cross_info_rate):
      '''Setter for the cross information rate
      
      :param cross_info_rate: New cross information rate ([0,1])
      :type cross_info_rate: float
      '''

      #Check the cross probability is between 0 and 1
      if(cross_info_rate < 0 or cross_info_rate > 1):
        raise Exception("Unexpected crossover information rate (not between 0 and 1) !") 
      self.__cross_info_rate = cross_info_rate

    def set_mutation_proba(self,mutation_proba):
      '''Setter for the mutation probability
      
      :param mutation_proba: New mutation probability ([0,1])
      :type mutation_proba: float
      '''

      #Check the mutation probability is between 0 and 1
      if(mutation_proba < 0 or mutation_proba > 1):
        raise Exception("Unexpected mutation probability (not between 0 and 1) !")
      self.__cross_proba = mutation_proba

    def set_select_number(self,select_number):
      '''Setter for the number of individual to select during the selection operation
      
      :param select_number: New select number
      :type select_number: integer
      '''

      self.__select_number = select_number

    def set_gen_number(self,gen_number):
      '''Setter for the number of generation the optimizer will process
      
      :param gen_number: New number of generation
      :type gen_number: integer
      '''

      self.__gen_number = gen_number

    def set_randomizer(self,randomizer):
      '''Setter for the randomizer of the optimizer
      
      :param randomizer: New randomizer value
      :type randomizer: boolean
      '''

      self.__randomizer = randomizer

    def fitness_history_record(self,fitnesses,gen_idx):
      '''Update the fitness history with a new fitness record and the corresponding generation as key
      
      :param fitnesses: Value added to the history. List containing the fitnesses of the new individuals of the generation (new fitnesses) 
      :type fitnesses: list
      :param gen_idx: Key added to the history. Number of the corresponding generation
      :type gen_idx: integer
      '''

      self.__fitness_history.update({gen_idx:fitnesses})

    def fitness_best_record(self,fitness):
      '''Update the best fitness history with the record of the best fitness ever. 
      
      :param fitness: Value added to the history. List containing the fitnesses of the new individuals of the generation (new fitnesses) 
      :type fitness: float
      '''

      self.__best_history.append(fitness)

    def init_individual(self,container,source_file):
      '''Method to initialize one individual (Grid) for the Optimizer
      
      :param container: Encapsulation structure for the Grid.
      :type container: container
      :param source_file: Vocabulary or file from which the grid will be generated.
      :type source_file: file or Dict
      :return: returns a container
      :rtype container: container
      '''
      #Create an encapsulated grid in the container to fit with the DEAP framework (from the source file)
      return container(source_file,root_name = "accueil",randomizer = self.get_randomizer(), dynamic_size = True)

    def init_population(self,container,func,source_file):
      '''Method to initialize the population of the Optimizer
      
      :param container: Encapsulation structure for the population.
      :type container: container
      :param source_file: Vocabulary or file from which the grid will be generated.
      :type source_file: file or Dict
      :return: returns a container
      :rtype container: container
      '''

      #Create a population of individuals. The size of the population is the initial population size. 
      return container(func(source_file) for i in range(self.get_pop_size()))


    def init_genetic_objects(self):
      '''Method that will initialize the objects for the genetic algorithm
      '''

      #Creator for the fitness and the individual types
      creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
      creator.create("Individual", Grid, fitness=creator.FitnessMin)
        
      #Individual definition
      self.__toolbox.register("individual", self.init_individual, creator.Individual)

      #Population definition (using initRepeat, we will generate a list of individual)
      self.__toolbox.register("population", self.init_population, list, self.__toolbox.individual)

    def production_cost(self,individual):
      '''Method used by the optimizer to evaluate one individual by using the production cost

      :param individual: The inidividual the optimizer will evaluate
      :type individual: individual
      :return: returns the production cost of the grid
      :rtype: (float,)
      '''
      return grid_cost(individual, self.get_eval_file(), average_option = self.get_cost_average(), distance_mode = self.get_distance_formula()),

    def pgcs_crossover_swap(self,ind_x, ind_y):
      '''Method used by the optimizer to perform a crossover between two individuals and generate a new one

      :param ind_x: The first individual for the crossover (parent x)
      :type ind_x: individual
      :param ind_y: The second individual for the crossover (parent y)
      :type ind_y: individual
      :return: returns the childs of the two parents (crossover result)
      :rtype: individual,individual
      '''

      #Get the two vocabulary from the two individual, respectively x and y
      voc_x = ind_x.get_core_voc()
      voc_y = ind_y.get_core_voc()

      #Initialization of empty lists to store the vocabulary in list
      list_voc_x = []
      list_voc_y = []
      identifiers = []

      #Store the dictionary from the first individual (x)
      for picto_x in voc_x.values():
        list_voc_x.append(picto_x)

      #Store the dictionary from the second individual (y)
      for picto_y in voc_y.values():
        list_voc_y.append(picto_y)

      #For every pictograms in the second individual (y)
      for slot_y in range(len(list_voc_y)):

        #Compute an independent probability to know if we have to give the information of the pictogram from y to x.
        if(random.random() < self.get_cross_info_rate()):

          #Save the word and the new position of the target pictogram
          target_word = list_voc_y[slot_y][0]
          new_row = list_voc_y[slot_y][1]
          new_col = list_voc_y[slot_y][2]

          #Find the position of this information in the first individual (x)
          i = 0
          for picto in list_voc_x:
            #Position of the target in x is found
            if(picto[0] == target_word):

              #Save position of the target in x
              target_row = picto[1]
              target_col = picto[2]
              target_save = picto
              #Save the slot
              slot_x = i

            #Position of the pictogram to swap
            if(picto[1] == new_row and picto[2] == new_col):

              picto_save = picto

            #Counter over the iterations
            i = i + 1

          #Swap of the two pictograms positions          
          picto_save[1] = target_row
          picto_save[2] = target_col
          target_save[1] = new_row
          target_save[2] = new_col

          #Swap the pictogram in the grid
          list_voc_x[slot_x], list_voc_x[slot_y] = list_voc_x[slot_y], list_voc_x[slot_x]

      #Store the identifiers of each pictogram
      for picto in list_voc_x:
        identifiers.append(picto[4])

      #Build the new vocabulary
      new_voc = dict(zip(identifiers,list_voc_x))

      #Modify the individual
      new_ind = self.__toolbox.individual(new_voc)

      return new_ind,new_ind

    def pgcs_mutation_swap(self,ind):
      '''Method used by the optimizer to perform a mutation on one individual
      The mutation will swap randomly two pictograms in the grid.

      :param ind: the individual subject to the mutation
      :type ind: individual
      :return: returns the individual after the mutation
      :rtype: individual
      '''
      #Get the vocabulary of the individual
      voc = ind.get_core_voc()

      #Initialization of empty lists to store the vocabulary
      list_voc = []
      identifiers = []

      #Store the dictionary in list format
      for picto in voc.values():
        list_voc.append(picto)
      
      #Get two random position of pictogram to swap
      slot_a = random.randint(0,len(list_voc) - 1)
      slot_b = random.randint(0,len(list_voc) - 1)

      #Get the two pictograms
      picto_a = list_voc[slot_a]
      picto_b = list_voc[slot_b]

      #Swap the real position of the pictogram (row,col values)
      tmp = (picto_a[1],picto_a[2])
      picto_a[1] = picto_b[1]
      picto_a[2] = picto_b[2]
      picto_b[1] = tmp[0]
      picto_b[2] = tmp[1]

      #Swap the pictogram in the grid
      list_voc[slot_a], list_voc[slot_b] = list_voc[slot_b], list_voc[slot_a]

      #Store the identifiers of each pictogram
      for picto in list_voc:
        identifiers.append(picto[4])

      #Build the new vocabulary
      new_voc = dict(zip(identifiers,list_voc))

      #Modify the individual
      new_ind = self.__toolbox.individual(new_voc)

      return new_ind

    def init_operations(self):
      '''Method that will initialize operations used by the genetic algorithm (evaluation, selection, crossover, mutation)
      '''

      #--Evaluation definition--
      self.__toolbox.register("evaluation", self.production_cost)

      #--Selection definition--

      #Using tools.selBest (select the k best individuals following the fitness)
      self.__toolbox.register("selection", tools.selBest) 

      #--Crossover definition--
      self.__toolbox.register("crossover",self.pgcs_crossover_swap)

      #--Mutation definition--
      self.__toolbox.register("mutation",self.pgcs_mutation_swap)
  

    def genetic_algorithm(self):
      '''Method that will use a genetic algorithm to generate an optimal grid starting from a random generation.

      :return: Returns the best individual of the last generation (optimized grid)
      :rtype: class: Grid
      '''

      #====INITIAL GENERATION====

      #Initialization of the population
      pop = self.__toolbox.population(self.get_source_file())

      #Initialization of the best individual
      best_ind = pop[0]
      best_gen = 0

      #Evaluation of the initial population
      fitnesses = list(map(self.__toolbox.evaluation,pop))
      min_init_fit = fitnesses[0]

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

      print("INITIAL GENERATION (0) --> Best fitness : " + str(best_ind.fitness.values[0]) + "\n")

      #==ITERATION OVER GENERATIONS==

      #Iterative process : For each generation
      for gen in tqdm(range(1,self.get_gen_number()+1),desc = "** Optimization **",unit = "generation"):

        #--SELECTION--

        #Select the k best individuals of the current generation
        offspring = self.__toolbox.selection(pop,self.get_select_number())
        # Clone the selected individuals
        offspring = list(map(self.__toolbox.clone, offspring))

        #--CROSSOVER--
        for ind1,ind2 in zip(offspring[::2], offspring[1::2]):

          #Probability to perform the crossover
          if(random.random() < self.get_cross_proba()):

            #Crossover operation to generate the new individual
            new_ind1,new_ind2 = self.__toolbox.crossover(ind2,ind1)
            offspring.append(new_ind1)
            offspring.append(new_ind2)

        #--MUTATION--
        for ind in offspring:

          #Probability to perform a mutation
          if(random.random() < self.get_mutation_proba()):

            #Mutation operation to modify the individual
            offspring.remove(ind)
            mutant = self.__toolbox.mutation(ind)
            offspring.append(mutant)

        #--EVALUATION--

        #Avoid useless computation
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

        #Evaluation of the population
        fitnesses = list(map(self.__toolbox.evaluation,invalid_ind))
        
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
      print("Best individual --> Generation : " + str(best_gen) + ", Fitness : " + str((self.__toolbox.evaluation(best_ind))[0]))

      return Grid(best_ind.get_core_voc())


    def display_config(self):
      '''Method to display the configuration of the optimizer
      '''

      #Display informations
      print("####### Genetic Pictogram Grid Communication Optimizer ######\n")
      print("## Optimizer Parameters ##")
      print("========================================================================")
      print("Source file : " + str(self.get_source_file()) + "     Evaluation file : " + str(self.get_eval_file()) + "\n")
      print("  INITIAL POPULATION SIZE : "+ str(self.get_pop_size())+"\n")
      print("  NUMBER OF GENERATION : "+ str(self.get_gen_number())+"\n")
      print("  CROSSOVER RATE : "+ str(self.get_cross_proba() * 100)+"%     MUTATION RATE : "+ str(self.get_mutation_proba() * 100)+"%\n")
      print("  CROSSOVER INFORMATION RATE : "+ str(self.get_cross_info_rate() * 100)+"%\n")
      print("  DISTANCE FORMULA (COST) : "+ str(self.get_distance_formula().upper()) + "\n")
      print("========================================================================\n")


    def fitness_history(self,option = "best"):
      '''Methods returning the fitness history depending on the request from the user (parameters)

      :param option: Option to know what the history will contain, optional ("best" by default)
      Possible options : "gen_best", "only_best", "average", "all"
      :type: string
      :return: Returns the prepared history depending of the options and the request from the user.
      :rtype: list
      '''

      #Initialization of the history
      history = []

      #Prepare the best fitness from each generation
      if(option == "gen_best"):
        for fitnesses in self.get_fitness_history().values():
          #Append the best fitness for each generation in the history to return (if the list is not empty)
          if(fitnesses):
            history.append(min(fitnesses)[0])

      #Prepare the best fitness evolution
      elif(option == "only_best"):
        #Append all recorded fitnesses.
        for fitness in self.get_best_history():
          if(fitness):
            history.append(fitness)

      #Prepare the average fitness from each generation
      elif(option == "average"):
        for fitnesses in self.get_fitness_history().values():
          #Append the average of the fitness for the generation in the history to return (if the list is not empty)
          if(fitnesses):
            history.append((sum(fitnesses[0]) / len(fitnesses[0])))

      #Prepare all fitnesses from each generation
      elif(option == "all"):
        for fitnesses in self.get_fitness_history().values():
          #Append all fitnesses for the generation in the history to return (if the list is not empty)
          if(fitnesses):
            for fitness in fitnesses:
              history.append(fitness[0])

      else:
        raise Exception("Invalid provided option") 
      
      return history