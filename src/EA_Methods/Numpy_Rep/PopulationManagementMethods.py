from random import random

# region Globals and Setters
genome_length = 0
population_method = None
eval_fitness = None
op = None
start_temp = 10000
cooling_rate = 0.995
population_threshold = 0.35


def set_genome_length(i):
    global genome_length
    genome_length = i


def set_population_method(i):
    global population_method
    population_method = i


def set_fitness_function(i):
    global eval_fitness
    eval_fitness = i


def set_op(i):
    global op
    op = i


def set_start_temp(i):
    global start_temp
    start_temp = i


def set_cooling_rate(i):
    global cooling_rate
    cooling_rate = i


def set_population_threshold(i):
    global population_threshold
    population_threshold = i
# endregion


# region Population Management Methods
# TODO - Optimize input as a sorted list, so that searching is not required.

# TODO - Determine if the decorators are needed.
def probabilistic_modification(func):
    def generate_output(population, fitness):
        best_fit = op(fitness)
        threshold = func()
        for x in range(genome_length):
            if fitness[x] == best_fit and random() < threshold:
                population[x] = population_method()
                fitness[x] = eval_fitness(population[x])

        return population, fitness
    return generate_output


def discretized_modification(func):
    def generate_output(population, fitness):
        pass
        return population, fitness
    return generate_output


def static_return(population, fitness):
    """
    Makes no changes to the population
    """
    return population, fitness


def metallurgic_annealing(population, fitness):
    """
    A function based on the principle of 'Annealing' in metalworking. While the algorithm is in
    its youth, we allow optimal answers to be replaced with new individuals based on a threshold
    probability which is gauged by the 'temperature' and 'cooling rate'
    """

    '''
    // Calculate the acceptance probability
    public static double acceptanceProbability(int energy, int newEnergy, double temperature) {
        // If the new solution is better, accept it
        if (newEnergy < energy) {
            return 1.0;
        }
        // If the new solution is worse, calculate an acceptance probability
        return Math.exp((energy - newEnergy) / temperature);
    '''

    '''
    class MyNumbers:
        def __iter__(self):
            self.a = 1
            return self

        def __next__(self):
            if self.a <= 20:
                x = self.a
                self.a += 1
                return x
            else:
                raise StopIteration
    '''
    pass


def entropic_stabilizing(population, fitness):
    """
    A process where the more individuals of the current best fitness there
    that exist, the more likely it is that the individuals are randomly
    replaced with new individuals,
    """

    best_fit = op(fitness)
    num_best = fitness.count(best_fit)

    if num_best > population_threshold:
        threshold = 0.8*((num_best - population_threshold) / (len(population) - population_threshold))
        for x in range(genome_length):
            if fitness[x] == best_fit and random() < threshold:
                population[x] = population_method()
                fitness[x] = eval_fitness(population[x])

    return population, fitness


def ouroboric_culling(population, fitness):
    """
    Like the snake of legend, as the algorithm grows and stabilizes,
    it ends up 'eating' itself. It does this by limiting the percent
    of individuals which can share the maximum fitness.
    """

    best_fit = op(fitness)
    num_best = fitness.count(best_fit)
    if num_best > population_threshold:
        num_to_remove = num_best - population_threshold
        for x in range(genome_length):
            if fitness[x] == best_fit:
                population[x] = population_method()
                fitness[x] = eval_fitness(population[x])
                num_to_remove -= 1
                if num_to_remove == 0:
                    break

    return population, fitness
# endregion
