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
    '''
    
    def __init__(self, source_file, pop_size = 10, cross_proba = 0.5, mutation_proba = 0.5, select_number = 2, gen_number = 10):
        '''Constructor
        '''

        self.__source_file = source_file
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

        #Genetic objects initialization
        self.__toolbox = base.Toolbox()
        self.init_genetic_objects()

        #Genetic operations initialization
        self.init_operations()

        #Display informations
        print("####### Genetic Pictogram Grid Communication Optimizer ######\n")
        print("  INITIAL POPULATION SIZE : "+ str(self.__pop_size)+"\n")
        print("  CROSSOVER RATE : "+ str(self.__cross_proba * 100)+"%\n")
        print("  MUTATION RATE : "+ str(self.__mutation_proba * 100)+"%\n")
        print("  NUMBER OF GENERATION : "+ str(self.__gen_number)+"\n")

    def get_source_file(self):
      '''Getter for the source file
      
      :return: Returns the source file name given as input
      :rtype: string
      '''

      return self.__source_file

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
      return container(source_file,root_name = "accueil",randomizer = True, dynamic_size = True)

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
      '''

      return grid_cost(individual, "input_cost.txt"),

    def pgcs_crossover(self,ind_a, ind_b):
      '''Method used by the optimizer to perform a crossover between two individuals and generate a new one
      '''

      voc_a = ind_a.get_core_voc()
      voc_b = ind_b.get_core_voc()

      new_ind = self.__toolbox.individual(voc_a)
      return new_ind

    def pgcs_mutation(self,ind):
      '''Method used by the optimizer to perform a mutation on one individual
      '''
      #Get the vocabulary of the individual
      voc = ind.get_core_voc().values()

      #Initialization of empty lists to store the vocabulary
      list_voc = []
      identifiers = []

      #Store the dictionary in list format
      for picto in voc:
        list_voc.append(picto)
      
      #Random shuffle the list (mutation)
      random.shuffle(list_voc)

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
      self.__toolbox.register("crossover",self.pgcs_crossover)

      #--Mutation definition--
      self.__toolbox.register("mutation",self.pgcs_mutation)
  

    def genetic_algorithm(self):
      '''Method that will use a genetic algorithm to generate an optimal grid starting from a random generation.
      '''

      #====INITIAL GENERATION====

      #Initialization of the population
      pop = self.__toolbox.population(self.get_source_file())

      #Evaluation of the initial population
      fitnesses = list(map(self.__toolbox.evaluation,pop))

      #For each individual in the population, associate the fitness to the individual
      for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit + (1,)

      print("GENERATION 0 (initial)")
      print("fitnesses :" + str(fitnesses))

      #==ITERATION OVER GENERATIONS==

      #Iterative process : For each generation
      for gen in range(1,self.get_gen_number()+1):
        print("GENERATION " + str(gen))

        #--SELECTION--

        #Select the k best individuals of the current generation
        offspring = self.__toolbox.selection(pop,self.get_select_number())

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
            modified_ind = self.__toolbox.mutation(ind)
            offspring.append(modified_ind)

        #--EVALUATION--

        #Evaluation of the population
        fitnesses = list(map(self.__toolbox.evaluation,offspring))
        print("fitnesses :" + str(fitnesses))

        #For each individual in the population, associate the fitness to the individual
        for ind, fit in zip(offspring, fitnesses):
          ind.fitness.values = fit

        #--NEW GENERATION--
        pop[:] = offspring
      
      #Final population
      return pop

