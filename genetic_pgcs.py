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

    :initial_grid: initial grid from what the optimizer will compute the optimized one
    :type initial_grid: class: Grid
    :pop_size: size of the initial population, optional (10 by default)
    :type pop_size: integer
    :cross_proba: probability of having a crossover between two individuals, optional (0.5 by default)
    :type cross_proba: float ([0,1])
    :mutation_proba: probability of having a mutation for one individual, optional (0.5 by default)
    :type mutation_proba: float ([0,1])
    :gen_number: number of generation the optimizer will process, optional (10 by default)
    :type gen_number: integer
    '''
    
    def __init__(self, initial_grid, pop_size = 10, cross_proba = 0.5, mutation_proba = 0.5, gen_number = 10):
        '''Constructor
        '''

        self.__initial_grid = initial_grid
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

        #Display informations
        print("####### Genetic Pictogram Grid Communication Optimizer ######\n")
        print("  INITIAL POPULATION SIZE : "+ str(self.__pop_size)+"\n")
        print("  CROSSOVER RATE : "+ str(self.__cross_proba * 100)+"%\n")
        print("  MUTATION RATE : "+ str(self.__mutation_proba * 100)+"%\n")
        print("  NUMBER OF GENERATION : "+ str(self.__gen_number)+"\n")

    def get_initial_grid(self):
      '''Getter for the initial grid
      
      :return: Returns the grid given as input
      :rtype: class: Grid
      '''

      return self.__initial_grid

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

    def set_initial_grid(self,initial_grid):
      '''Setter for the initial grid
      
      :param: New initial grid given to the optimizer
      :type: class: Grid
      '''

      self.__initial_grid = initial_grid

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
    
