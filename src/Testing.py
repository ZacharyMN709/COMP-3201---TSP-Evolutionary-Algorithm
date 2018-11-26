from src.EA_Shell import EARunner
from src.StatsHolder import StatsHolder
from multiprocessing import Process


class EATester(EARunner):
    def __init__(self, PSM, RM, MM, SSM, DEF, PMM, mt=False):
        super().__init__(PSM, RM, MM, SSM, DEF, PMM)
        self.RUNS = None
        self.POPULATION_METHODS = None
        self.PARENT_METHODS = None
        self.RECOMBINATION_METHODS = None
        self.MUTATION_METHODS = None
        self.SURVIVOR_METHODS = None
        self.MANAGEMENT_METHODS = None
        self.testable = False
        self.multithread = mt
        self.processes = []
        self.running = 0

    def set_test_vars(self, runs, pop, par, rec, mut, sur, man):
        self.RUNS = runs
        self.POPULATION_METHODS = pop
        self.PARENT_METHODS = par
        self.RECOMBINATION_METHODS = rec
        self.MUTATION_METHODS = mut
        self.SURVIVOR_METHODS = sur
        self.MANAGEMENT_METHODS = man

        self.testable = pop and par and rec and mut and sur and runs and man

    def iterate_tests(self, generation_limit, known_optimum=None, true_opt=False, print_gens=0):
        def run_test(v, w, x, y, z, a, i, id):
            if self.multithread:
                print('Thread {} Started'.format(id))
            else:
                print('Test {} Started'.format(id))
            self.set_params(self.genome_length, self.eval_fitness,
                            self.POPULATION_METHODS[v][1], self.PARENT_METHODS[w][1], self.RECOMBINATION_METHODS[x][1],
                            self.MUTATION_METHODS[y][1], self.SURVIVOR_METHODS[z][1], self.MANAGEMENT_METHODS[a][1])
            op_fit, best_indivs, gencount, run_history, time_tuple = \
                self.run(generation_limit, known_optimum, true_opt, print_gens if not self.multithread else False, True)

            matrix[v][w][x][y][z][a].set_run_stats(i, op_fit, best_indivs, gencount, run_history, time_tuple)
            if self.multithread:
                print('Thread {} finished running!'.format(id))
                print(matrix[v][w][x][y][z][a].funcs_used())
                matrix[v][w][x][y][z][a].print_simple_stats()
            print("\n -------- \n")


        if not self.testable:
            print("Error! Missing information to run tests. Please check the code for errors.")
            return

        # Stats Set-up
        matrix = [[[[[[StatsHolder(self.POPULATION_METHODS[v][0],
                                   self.PARENT_METHODS[w][0],
                                   self.SURVIVOR_METHODS[z][0],
                                   self.MUTATION_METHODS[y][0],
                                   self.RECOMBINATION_METHODS[x][0],
                                   self.MANAGEMENT_METHODS[a][0],
                                   self.RUNS,
                                   self.op,
                                   known_optimum if true_opt else None)
                       # matrix[v][w][x][y][z][a] returns a object corresponding to the functions used
                       for a in range(len(self.MANAGEMENT_METHODS))]
                      for z in range(len(self.SURVIVOR_METHODS))]
                     for y in range(len(self.MUTATION_METHODS))]
                    for x in range(len(self.RECOMBINATION_METHODS))]
                   for w in range(len(self.PARENT_METHODS))]
                  for v in range(len(self.POPULATION_METHODS))]

        # EA Iterator
        for v in range(len(self.POPULATION_METHODS)):
         for w in range(len(self.PARENT_METHODS)):
          for x in range(len(self.RECOMBINATION_METHODS)):
           for y in range(len(self.MUTATION_METHODS)):
            for z in range(len(self.SURVIVOR_METHODS)):
             for a in range(len(self.MANAGEMENT_METHODS)):
              for i in range(self.RUNS):
               if self.multithread:
                # Spawn a new process to run the algorithm
                process_id = len(self.processes)
                print('Thread {} Initialized'.format(process_id))
                process = Process(target=run_test, args=(v, w, x, y, z, a, i, process_id))
                self.processes.append(process)
               else:
                run_test(v, w, x, y, z, a, i, self.running)
                self.running += 1
               print(matrix[v][w][x][y][z][a].funcs_used())


        if self.multithread:
            # Start processes
            for process in self.processes:
                process.start()
            # Wait for processes to finish
            for process in self.processes:
                process.join()


        # Stats Output
        if not self.multithread:
         for v in range(len(self.POPULATION_METHODS)):
          for w in range(len(self.PARENT_METHODS)):
           for x in range(len(self.RECOMBINATION_METHODS)):
            for y in range(len(self.MUTATION_METHODS)):
             for z in range(len(self.SURVIVOR_METHODS)):
              for a in range(len(self.MANAGEMENT_METHODS)):
               print("After {} iterations, with {} generations per iteration".format(self.RUNS, generation_limit))
               print(matrix[v][w][x][y][z][a].funcs_used())
               matrix[v][w][x][y][z][a].print_simple_stats()
               print("\n -------- \n")

        return matrix, (v, w, x, y, z, a)
