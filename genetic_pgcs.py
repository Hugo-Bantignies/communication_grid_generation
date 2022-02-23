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
from mimetypes import init
from communication_grid import Grid

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
    :gen_number: number of generation the optimizer will process, optional (10 by default)
    :type gen_number: integer
    '''
    
    def __init__(self, source_file, pop_size = 10, cross_proba = 0.5, mutation_proba = 0.5, gen_number = 10):
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

        self.__gen_number = gen_number

        #Genetic objects initialization
        self.__toolbox = base.Toolbox()
        self.init_genetic_objects()

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

    def get_gen_number(self):
      '''Getter for the number of generation the optimizer will process
      
      :return: Returns the number of generations
      :rtype: intger
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

    def set_pop_size(self,gen_number):
      '''Setter for the number of generation the optimizer will process
      
      :param: New number of generation
      :type: integer
      '''

      self.__gen_number = gen_number

    def init_individual(self,container):
      '''Method to initialize one individual (Grid) for the Optimizer
      
      :param container: Encapsulation structure for the Grid.
      :type container: container
      :return: returns a container
      :rtype container: container
      '''
      #Create an encapsulated grid in the container to fit with the DEAP framework
      return container(self.get_source_file(),"accueil",randomizer = True, dynamic_size = True)

    def init_genetic_objects(self):
      '''Method that will initialize the objects for the genetic algorithm
      '''

      #Creator for the fitness and the individual types
      creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
      creator.create("Individual", Grid, fitness=creator.FitnessMin)
        
      #Individual definition
      self.__toolbox.register("individual", self.init_individual, creator.Individual)

      #Population definition (using initRepeat, we will generate a list of individual)
      self.__toolbox.register("population", tools.initRepeat, list, self.__toolbox.individual)

    def genetic_algorithm(self):

      #Initialization of the population
      pop = self.__toolbox.population(self.get_pop_size())

      #Print the population
      for i in range(self.get_pop_size()):
        print(pop[i].__str__())

