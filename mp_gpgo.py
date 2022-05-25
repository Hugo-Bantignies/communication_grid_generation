from gpgo import gpgo,load_gpgo
from tqdm import tqdm

#Paralellization
import multiprocessing as mp

#===============================================
# MULTIPROCESSING OF THE GENETIC ALGORITHM
#===============================================


class mp_gpgo():
    
    def __init__(self, source_files, evaluation_files, config_files, nb_proc = 0):

        self.source_files = source_files
        
        #The evaluation file has to be a .txt file.
        if(evaluation_files[0].endswith('.txt')):
            self.evaluation_files = evaluation_files

        #File format not accepted
        else:
            raise Exception("Not accepted evaluation file format !")

        self.config_files = config_files

        #Set the number of process
        if(nb_proc <= 0):
          self.nb_proc = mp.cpu_count()
        else:
          self.nb_proc = nb_proc

        self.final_results = None

        #Load one optimizer to initialize the DEAP objects
        init_deap = load_gpgo(self.source_files, self.evaluation_files, self.config_files[0])

    def mp_optimization_pipeline(self,pid):
      '''Function to execute the genetic_algorithm for one process
      '''

      #New genetic optimizer
      optimizer = load_gpgo(self.source_files, self.evaluation_files, self.config_files[pid%len(self.config_files)])

      #Optimization and return the best grid
      optimal_grid = optimizer.genetic_algorithm(pid)

      return optimal_grid[0],optimal_grid[1],optimizer.best_history

    def mp_fitness_history(self):
        '''Method to get the best history from each processes'''

        history = []

        for result in self.final_results:

            history.append(result[2])

        return history

    def mp_genetic_algorithm(self):
      '''Function to run several times on several CPU cores the genetic algorithm
      '''

      # Windows support
      mp.freeze_support()

      #Processes id
      pids = []
      for i in range(self.nb_proc):
        pids.append(i)
        
      #--MULTIPROCESSING--

      #Pool creation
      pool = mp.Pool(self.nb_proc,initargs=(mp.RLock(),), initializer=tqdm.set_lock)

      #Pool starting
      self.final_results = list(pool.imap(func = self.mp_optimization_pipeline,iterable = pids))

      #End of the pool
      pool.close()
      pool.join()

      #Return the best grid
      best_grid = self.final_results[0][0]
      best_fitness = self.final_results[0][1]

      for result in self.final_results:
          
          
          if(result[1] < best_fitness):

              best_grid = result[0]
              best_fitness = result[1]

      return best_grid