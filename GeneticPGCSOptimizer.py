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
import random
from mimetypes import init
from communication_grid import Grid
from evaluation_cost import *

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
    :mutation_proba: probability of having a mutation for one individual, optional (0.5 by default)
    :type mutation_proba: float ([0,1])
    :select_number: number of individual to select during the selection, optional (2 by default)
    :type select_number: integer
    :gen_number: number of generation the optimizer will process, optional (10 by default)
    :type gen_number: integer
    :randomizer: if True, the initial population of the grid will contain random grids, else the grids will follow the source_file, optional (True by default)
    :type gen_number: boolean
    '''
    
    def __init__(self, source_file, eval_file, pop_size = 10, cross_proba = 0.5, mutation_proba = 0.5, select_number = 2, gen_number = 10, randomizer = True):
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

        #Check the mutation probability is between 0 and 1
        if(mutation_proba < 0 or cross_proba > 1):
            raise Exception("Unexpected mutation probability (not between 0 and 1) !") 
        self.__mutation_proba = mutation_proba

        self.__select_number = select_number

        self.__gen_number = gen_number

        self.__randomizer = randomizer

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

    def set_source_file(self,source_file):
      '''Setter for the source file name
      
      :param: New source file name given to the optimizer
      :type: string
      '''

      self.__source_file = source_file

    def set_pop_size(self,pop_size):
      '''Setter for the size of the population
      
      :param: New population size
      :type: integer
      '''

      self.__pop_size = pop_size

    def set_cross_proba(self,cross_proba):
      '''Setter for the cross probability
      
      :param: New cross probability ([0,1])
      :type: float
      '''

      #Check the cross probability is between 0 and 1
      if(cross_proba < 0 or cross_proba > 1):
        raise Exception("Unexpected crossover probability (not between 0 and 1) !")
      self.__cross_proba = cross_proba

    def set_mutation_proba(self,mutation_proba):
      '''Setter for the mutation probability
      
      :param: New mutation probability ([0,1])
      :type: float
      '''

      #Check the mutation probability is between 0 and 1
      if(mutation_proba < 0 or mutation_proba > 1):
        raise Exception("Unexpected mutation probability (not between 0 and 1) !")
      self.__cross_proba = mutation_proba

    def set_select_number(self,select_number):
      '''Setter for the number of individual to select during the selection operation
      
      :param: New select number
      :type: integer
      '''

      self.__select_number = select_number

    def set_gen_number(self,gen_number):
      '''Setter for the number of generation the optimizer will process
      
      :param: New number of generation
      :type: integer
      '''

      self.__gen_number = gen_number

    def set_randomizer(self,randomizer):
      '''Setter for the randomizer of the optimizer
      
      :param: New randomizer value
      :type: boolean
      '''

      self.__randomizer = randomizer

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

      return grid_cost(individual, self.get_eval_file()),

    def pgcs_crossover_swap(self,ind_x, ind_y):
      '''Method used by the optimizer to perform a crossover between two individuals and generate a new one

      :param ind_x: The first individual for the crossover (parent x)
      :type ind_x: individual
      :param ind_y: The second individual for the crossover (parent y)
      :type ind_y: individual
      :return: returns the child of the two parents (crossover result)
      :rtype: individual
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

      #Get the random position of the information provided by the second individual (y)
      slot_y = random.randint(0,len(list_voc_y) - 1)

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

      return new_ind

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

      #Evaluation of the initial population
      fitnesses = list(map(self.__toolbox.evaluation,pop))

      #For each individual in the population, associate the fitness to the individual
      for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

      print("***GENERATION 0 (initial)***")
      print("fitnesses :" + str(fitnesses))

      #==ITERATION OVER GENERATIONS==

      #Iterative process : For each generation
      for gen in range(1,self.get_gen_number()+1):
        print("***GENERATION " + str(gen) + "***")

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
            new_ind = self.__toolbox.crossover(ind1,ind2)
            offspring.append(new_ind)

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

        #For each new individual in the population, associate the fitness to the individual
        for ind, fit in zip(invalid_ind, fitnesses):
          ind.fitness.values = fit

        #--NEW GENERATION--
        pop[:] = offspring
      
      #Final best grid
      final_ind = self.__toolbox.selection(pop,1)
      print("Best fitness : " + str(self.__toolbox.evaluation(final_ind[0])))

      return Grid(final_ind[0].get_core_voc())


    def display_config(self):
      '''Method to display the configuration of the optimizer
      '''

      #Display informations
      print("####### Genetic Pictogram Grid Communication Optimizer ######\n")
      print("Source file : " + str(self.get_source_file()) + "     Evaluation file : " + str(self.get_eval_file()) + "\n")
      print("  INITIAL POPULATION SIZE : "+ str(self.get_pop_size())+"\n")
      print("  CROSSOVER RATE : "+ str(self.get_cross_proba() * 100)+"%\n")
      print("  MUTATION RATE : "+ str(self.get_mutation_proba() * 100)+"%\n")
      print("  NUMBER OF GENERATION : "+ str(self.get_gen_number())+"\n")


