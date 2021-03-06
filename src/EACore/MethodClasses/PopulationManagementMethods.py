from src.EACore.MethodClasses.HelperTemplate import BaseHelper
from random import random, randint


class PopulationManagementHelper(BaseHelper):
    """
    These functions are either function derived from research online, or created by team
    members in an attempt to escape being stuck at local optima.
    """
    def __init__(self, var_helper):
        """
        :param var_helper: A reference to an EAVarHelper instance.
        """
        name_method_pairs = [('None', self.static_return),
                             ('Annealing', self.metallurgic_annealing),
                             ('Entropy', self.entropic_stabilizing),
                             ('Oroborous', self.ouroboric_culling),
                             ('Engineering', self.genetic_engineering)
                             ]
        super().__init__(var_helper, name_method_pairs)

    def __str__(self):
        return super().__str__().format('PopulationManagementHelper')

    # region Population Management Methods
    @staticmethod
    def static_return(population, fitness):
        """
        Makes no changes to the population
        :param population: The list of individuals from the EA
        :param fitness: The fitnesses of the individuals.
        :return: The modified population, and the modified fitnesses.
        """
        return population, fitness

    def metallurgic_annealing(self, population, fitness):
        """
        A function based on the principle of 'Annealing' in metalworking. While the algorithm is in
        its youth, we allow optimal answers to be replaced with new individuals based on a threshold
        probability which is gauged by the 'temperature' and 'cooling rate'
        :param population: The list of individuals from the EA
        :param fitness: The fitnesses of the individuals.
        :param start_temp: Set in the EAVarHelper class. The initial temperature of the 'metal'.
        :param cooling_rate: Set in the EAVarHelper class. The rate at which the 'metal' cools.
        :return: The modified population, and the modified fitnesses.
        """

        self.vars.start_temp *= self.vars.cooling_rate

        new_pop = [self.vars.make_new_individual() for _ in range(self.vars.population_size)]
        new_fit = [self.vars.eval_fitness(x) for x in new_pop]

        for x in range(len(population)):
            if self.vars.better_than(new_fit[x], fitness[x]) or random() < 2.7182818 ** (
                    (fitness[x] - new_fit[x]) / self.vars.start_temp):
                population[x] = new_pop[x]

        return population, fitness

    def entropic_stabilizing(self, population, fitness):
        """
        A process where the more individuals of the current best fitness there
        that exist, the more likely it is that the individuals are randomly
        replaced with new individuals,
        :param population: The list of individuals from the EA
        :param fitness: The fitnesses of the individuals.
        :param population_threshold: Set in the EAVarHelper class. The number of individuals who have the same fitness
        required for the function to modify individuals.
        :return: The modified population, and the modified fitnesses.
        """

        best_fit = self.vars.best_of(fitness)
        num_best = fitness.count(best_fit)

        if num_best > self.vars.population_threshold:
            threshold = 0.8 * ((num_best - self.vars.population_threshold) / (
                    self.vars.population_size - self.vars.population_threshold))
            for x in range(self.vars.genome_length):
                if fitness[x] == best_fit and random() < threshold:
                    population[x] = self.vars.make_new_individual()
                    fitness[x] = self.vars.eval_fitness(population[x])

        return population, fitness

    def ouroboric_culling(self, population, fitness):
        """
        Like the snake of legend, as the algorithm grows and stabilizes,
        it ends up 'eating' itself. It does this by limiting the percent
        of individuals which can share the maximum fitness.
        :param population: The list of individuals from the EA
        :param fitness: The fitnesses of the individuals.
        :param population_threshold: Set in the EAVarHelper class. The number of individuals who have the same fitness
        required for the function to modify individuals.
        :return: The modified population, and the modified fitnesses.
        """

        best_fit = self.vars.best_of(fitness)
        num_best = fitness.count(best_fit)
        if num_best > self.vars.population_threshold:
            num_to_remove = num_best - self.vars.population_threshold
            for x in range(self.vars.genome_length):
                if fitness[x] == best_fit:
                    population[x] = self.vars.make_new_individual()
                    fitness[x] = self.vars.eval_fitness(population[x])
                    num_to_remove -= 1
                    if num_to_remove == 0:
                        break

        return population, fitness

    def genetic_engineering(self, population, fitness):
        """
        Shuffle all of the genes next to each other, and see if it improves.
        If not, revert that change. Super charges a single fittest individual.
        Makes no changes to the population
        :param population: The list of individuals from the EA
        :param fitness: The fitnesses of the individuals.
        :param population_threshold: Set in the EAVarHelper class. The number of individuals who have the same fitness
        required for the function to modify individuals.
        :return: The modified population, and the modified fitnesses.
        """
        best_fit = self.vars.best_of(fitness)
        num_best = fitness.count(best_fit)

        if num_best > self.vars.population_threshold:
            x = randint(1, 10)
            index = fitness.index(best_fit)
            indiv = population[index]
            for i in range(len(indiv)):
                indiv[i - x], indiv[i] = indiv[i], indiv[i - x]
                new_fit = self.vars.eval_fitness(indiv)
                if new_fit == self.vars.best_of(new_fit, best_fit):
                    best_fit = new_fit
                else:
                    indiv[i - x], indiv[i] = indiv[i], indiv[i - x]

        return population, fitness
    # endregion
