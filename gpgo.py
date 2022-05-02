import random
from PictogramGrid import Grid
from EvaluationGrid import *
from tqdm import tqdm

#Paralellization
import multiprocessing as mp

#DEAP Framework (Genetic Algorithm)
from deap import base
from deap import creator
from deap import tools


class gpgo():
    '''Object that will compute an optimized grid from an initial grid using 
       an Evolutionary Algorithm (Genetic Algorithm) for a Pictogram Grid Communication System (PGCS)

    :source_files: source_files name or corpus from the one the optimizer will generate an optimal grid (`.txt`,`.csv`, Augcom)
    :type source_files: string
    :training_files: training file name to train the optimization of the grid.
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
    '''
    
    def __init__(self, source_files, training_files, pop_size = 10, cross_proba = 0.5, cross_info_rate = 0.5,
                 mutation_proba = 0.5, select_number = 2, gen_number = 10, randomizer = True):
        '''Constructor
        '''

        self.source_files = source_files
        
        #The evaluation file has to be a .txt file.
        if(training_files[0].endswith('.txt')):
            self.training_files = training_files

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
        
        self.fitness_history = dict()

        self.best_history = []

        #Genetic objects initialization
        self.toolbox = base.Toolbox()
        self.init_genetic_objects()

        #Genetic operations initialization
        self.init_operations()

    def fitness_history_record(self,fitnesses,gen_idx):
      '''Update the fitness history with a new fitness record and the corresponding generation as key
      
      :param fitnesses: Value added to the history. List containing the fitnesses of the new individuals of the generation (new fitnesses) 
      :type fitnesses: list
      :param gen_idx: Key added to the history. Number of the corresponding generation
      :type gen_idx: integer
      '''

      self.fitness_history.update({gen_idx:fitnesses})

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
      return container(source_files,root_name = "accueil",randomizer = self.randomizer,warnings = False)

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
      return grid_distance_cost(individual, self.training_files),

    def pgcs_crossover_swap(self,ind_x, ind_y):
      '''Method used by the optimizer to perform a crossover between two individuals and generate a new one

      :param ind_x: The first individual for the crossover (parent x)
      :type ind_x: individual
      :param ind_y: The second individual for the crossover (parent y)
      :type ind_y: individual
      :return: returns the childs of the two parents (crossover result)
      :rtype: individual,individual
      '''

      return ind_x,ind_y

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
      if(selected_picto_a.is_directory == False and selected_picto_b.is_directory == False and selected_picto_a.word != selected_picto_b.word):
        ind.swap_pictograms(selected_picto_a,selected_picto_b)

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
      self.toolbox.register("crossover",self.pgcs_crossover_swap)

      #--Mutation definition--
      self.toolbox.register("mutation",self.mutation_swap_picto_inter)
  

    def genetic_algorithm(self):
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

      #print("DEBUG : INITIAL GENERATION (0) --> Best fitness : " + str(best_ind.fitness.values[0]) + "\n")

      #==ITERATION OVER GENERATIONS==

      #Iterative process : For each generation
      for gen in tqdm(range(1,self.gen_number+1),desc = "Optimization : ",unit = "generation"):

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
      print("DEBUG : Best individual --> Generation : " + str(best_gen) + ", Fitness : " + str((self.toolbox.evaluation(best_ind))[0]))
      return best_ind

    #===============================================
    # DISPLAY METHODS
    #===============================================

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
        print("------------------------------------------------------------------------")
        print("========================================================================\n")