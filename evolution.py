import tsplib95
import random
import numpy
from enum import Enum

tspProblem = tsplib95.load('berlin52.tsp')


class SurvivalSelectionType(Enum):
    PLUS_SELECTION = 1,
    COMMA_SELECTION = 2


class Individual:
    def __init__(self, path: list[int]):
        self.path = path

    def get_fitness(self):
        fitness = 0
        for count in range(len(self.path) - 1):
            fitness += tspProblem.get_weight(self.path[count], self.path[count + 1])

        # Return to start point
        fitness += tspProblem.get_weight(self.path[len(self.path)-1], self.path[0])
        return fitness

    def get_return_path(self):
        return_list = self.path.copy()
        return_list.append(self.path[0])
        return return_list

    def randomize_path(self):
        random.shuffle(self.path)

    def mutate(self):
        # Replace a random node with another random note
        node_to_replace = random.choice(self.path)
        node_to_replace_with = random.choice(self.path)
        index_to_replace = self.path.index(node_to_replace)
        index_to_replace_with = self.path.index(node_to_replace_with)
        self.path[index_to_replace] = node_to_replace_with
        self.path[index_to_replace_with] = node_to_replace


class Population:
    population: list[Individual] = []
    path = list(tspProblem.get_nodes())

    def __init__(self, population_size: int):
        self.population_size = population_size

        for count in range(population_size):
            temp = Individual(self.path.copy())
            temp.randomize_path()
            self.population.append(temp)

    # Param for Plus or Comma Selection
    def survival_selection(self, selection_type: SurvivalSelectionType, children: list[Individual]):
        if selection_type == SurvivalSelectionType.COMMA_SELECTION:
            # The best only from children
            self.population = children
            self.select_best()

        else:
            # The best of both
            self.population = self.population + children
            self.select_best()

    def select_best(self):
        ranking_list: list[(Individual, int)] = []
        # List to sort by fitness
        for x in self.population:
            ranking_list.append((x, x.get_fitness()))

        ranking_list = self.sort_tuple_list(ranking_list)
        best_individuals = []

        # Select the best and create the new population
        for y in range(self.population_size):
            best_individuals.append(ranking_list[y][0])
        self.population = best_individuals

    def sort_tuple_list(self, tuple_list: list[tuple]):
        tuple_list.sort(key=lambda x: x[1])
        return tuple_list

    # Currently only random parents
    # Currently only one partner for each other
    # Select best parents together
    def mating_selection(self, children_count: int):
        parent_count = int(children_count / 2)
        parent_tuple: list[(Individual, Individual)] = []

        available_parents = self.population.copy()
        for count in range(0, parent_count):
            parent_one = random.choice(available_parents)
            available_parents.remove(parent_one)
            parent_two = random.choice(available_parents)
            available_parents.remove(parent_two)
            parent_tuple.append((parent_one, parent_two))

        return parent_tuple

    # Param for chance to mutate
    # Param how many crossover points
    def variation(self, parents, crossover_points: int, standard_deviation: float):

        # Crossover
        children = self.crossover(parents, crossover_points)

        temp_list = []

        # Chance for random mutation
        for child in children:
            mutations_per_child = abs(int(numpy.random.normal(0, standard_deviation)))
            for x in range(0, mutations_per_child):
                child.mutate()

            temp_list.append(child)

        return temp_list

    def crossover(self, parents, crossover_points: int):
        # At least one cross
        crossover_points += 1
        crossover_points = max(crossover_points, 2)

        # Crossover Algo implementation
        crosses_parent_one = numpy.array_split(parents[0].path, crossover_points)
        crosses_parent_two = numpy.array_split(parents[1].path, crossover_points)

        first_child_path = self.cross_arrays(crosses_parent_one, crosses_parent_two)
        second_child_path = self.cross_arrays(crosses_parent_two, crosses_parent_one)

        first_child = Individual(first_child_path)
        second_child = Individual(second_child_path)

        children = (first_child, second_child)
        return children

    def cross_arrays(self, array_one, array_two):
        new_crosses: list[list[int]] = []
        for number in range(0, len(array_one)):
            # Even
            if number % 2 == 0:
                new_crosses.append(array_one[number])
            # Odd
            else:
                new_crosses.append(array_two[number])

        new_path = []
        for arr in new_crosses:
            new_path = [*new_path, *arr]

        # Check if a value is missing and add at the end
        for temp_node_add in self.path:
            if not new_path.__contains__(temp_node_add):
                new_path.append(temp_node_add)

        # Check for duplicate values and remove
        for temp_node_remove in self.path:
            count_of_node = new_path.count(temp_node_remove)
            if count_of_node > 1:
                for i in range(1, count_of_node):
                    new_path.remove(temp_node_remove)
        return new_path

    # Add other params
    def evolutionary_algorithm(self, repetitions: int, crossover_points: int, standard_deviation: float):

        # Repeat x times for the generations
        for count in range(0, repetitions):
            parent_pairs = self.mating_selection(self.population_size)
            children = []
            for parent_pair in parent_pairs:
                temp = self.variation(parent_pair, crossover_points, standard_deviation)
                children.append(temp[0])
                children.append(temp[1])

            self.survival_selection(SurvivalSelectionType.PLUS_SELECTION, children.copy())
            # TODO Remove
            # print("Best from " + str(count) + " generation")
            # print(self.population[0].get_fitness())

        for indi in self.population:
            print(indi.get_fitness(), indi.get_return_path())
