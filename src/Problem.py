import random
from typing import List

import tsplib95
import heapq
import matplotlib.pyplot as plt



class Problem:
    def __init__(self, problem_path, parent_mu, children_lambda, mutation_probability, starting_population_multipliyer):
        self.problem : tsplib95.models.StandardProblem = tsplib95.load(problem_path)
        self.parent_mu = parent_mu
        self.children_lambda = children_lambda
        self.mutation_probability = 1 / self.problem.dimension
        self.starting_population_size = self.parent_mu * starting_population_multipliyer

        self.best_of_generation = []

        self.fig = None
        self.ax = None

    def init_population(self, starting_population_size):
        initial_population = []
        for i in range(starting_population_size):
            random_path = self.gen_random_path()
            heapq.heappush(initial_population, (self.calc_fitness(random_path), random_path))

        return initial_population

    def gen_random_path(self):
        cities = list(range(1, self.problem.dimension + 1))
        random.shuffle(cities)
        cities.append(cities[0])

        return cities

    def mutation_operator(self, path, mutation_probability):
        res = path
        for i in range(len(res) - 2):
            if random.random() < mutation_probability:
                temp = res[i]
                random_selector = random.choice(list(range((len(res) - 2))))
                res[i] = res[random_selector]
                res[random_selector] = temp

        res[len(res) - 1] = res[0]

        return res

    def order_crossover_recombination_operator(self, parent1: List[int], parent2: List[int]):
        lower_bound = random.randrange(0, len(parent1) - 2)
        upper_bound = random.randrange(lower_bound, len(parent1) - 2)
        return self._order_crossover_recombination_operator(parent1, parent2, lower_bound, upper_bound)

    def _order_crossover_recombination_operator(self, parent1, parent2, lower_bound, upper_bound):
        child_direct = parent1.copy()
        child_inverse = parent2.copy()
        inserted_direct = set(parent1[lower_bound:upper_bound + 1])
        inserted_inverse = set(parent2[lower_bound:upper_bound + 1])

        for i in range(len(parent1)):
            if i < lower_bound or i > upper_bound:
                for elem in parent2:
                    if elem not in inserted_direct:
                        child_direct[i] = elem
                        inserted_direct.add(elem)
                        break

        for i in range(len(parent1)):
            if i < lower_bound or i > upper_bound:
                for elem in parent1:
                    if elem not in inserted_inverse:
                        child_inverse[i] = elem
                        inserted_inverse.add(elem)
                        break

        return child_direct, child_inverse

    def selection_operator(self, generation):
        survivors = []
        num_parents = min(self.parent_mu, len(generation))
        for _ in range(num_parents):
            survivors.append(heapq.heappop(generation))

        return survivors

    def tournament_selection_operator(self, generation, tournament_size):
        survivors = []
        num_parents = min(self.parent_mu, len(generation))

        for _ in range(num_parents):
            tournament = random.sample(generation, tournament_size)
            winner = min(tournament, key=lambda x: x[0])
            generation.remove(winner)
            survivors.append(winner)

        return survivors

    def nearest_neighbors(self, start):
        visited = set()
        path = [start]
        visited.add(start)
        current = start

        while len(path) != self.problem.dimension:
            next_node = None
            min_cost = float('inf')

            for i, cost in enumerate(self.problem.edge_weights[current]):
                if i not in visited and cost < min_cost:
                    min_cost = cost
                    next_node = i

            if next_node is None:
                break

            current = next_node
            path.append(current)
            visited.add(current)

        path.append(start)
        return path

    def calc_fitness(self, path):
        fitness = 0

        for i in range(len(path) - 1):
            # fitness += self.problem.edge_weights[path[i] - 1][path[i + 1] - 1]
            fitness += self.problem.get_weight(path[i], path[i + 1])

        return fitness

    def gen_new_gen(self, old_gen):
        best_parents = self.selection_operator(old_gen)
        next_gen = []

        for i in range(self.children_lambda):
            child_1, child_2 = self.order_crossover_recombination_operator(random.choice(best_parents)[1], random.choice(best_parents)[1])
            mutated_child_1 = self.mutation_operator(child_1, self.mutation_probability)
            heapq.heappush(next_gen, (self.calc_fitness(mutated_child_1), mutated_child_1))
            mutated_child_2 = self.mutation_operator(child_2, self.mutation_probability)
            heapq.heappush(next_gen, (self.calc_fitness(mutated_child_2), mutated_child_2))

        for i in range(len(best_parents) - 1):
            heapq.heappush(next_gen, best_parents[i])

        # for _ in range(100):
        #     path = self.gen_random_path()
        #     heapq.heappush(next_gen, (self.calc_fitness(path), path))

        return next_gen


    def _find_best_path(self):
        generation = self.init_population(self.starting_population_size)
        generation_counter = 0

        while True:
            generation = self.gen_new_gen(generation)
            generation_counter += 1
            print("Generation #" + str(generation_counter) + " " + str(generation[0]))
            if generation_counter % 10 == 0:
                self.plot_tour(generation[0][1], generation[0][0], generation_counter)

    def find_best_path(self):
        self._find_best_path()


    def plot_tour(self, path, cost, generation):
        if self.problem.edge_weight_type == "EXPLICIT":
            points = {node: self.problem.display_data[node] for node in self.problem.get_nodes()}
        elif self.problem.edge_weight_type == "EUC_2D":
            points = {node: self.problem.node_coords[node] for node in self.problem.get_nodes()}
        else:
            raise ValueError(f'Unknown edge_weight_type {self.problem.edge_weight_type}')

        if self.fig is None:
            self.fig, self.ax = plt.subplots()
            self.ax.set_title("TSP Tour Generation: " + str(generation) + "Cost: " + str(cost))
            self.ax.grid(True)

        self.ax.cla()
        self.ax.grid(True)
        self.ax.set_title("TSP Tour Generation: " + str(generation) + " Cost: " + str(cost))

        x_coords, y_coords = zip(*[points[node] for node in path])
        self.ax.scatter(x_coords, y_coords, color='blue')

        for i in range(len(path) - 1):
            x1, y1 = points[path[i]]
            x2, y2 = points[path[i + 1]]
            self.ax.plot([x1, x2], [y1, y2], 'b-')

        if path[0] == path[-1]:
            x_start, y_start = points[path[0]]
            x_end, y_end = points[path[-1]]
            self.ax.plot([x_end, x_start], [y_end, y_start], 'b-')

        plt.pause(0.1)






