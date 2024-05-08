import asyncio
import random
from typing import List

import tsplib95
import heapq
import matplotlib.pyplot as plt


class Problem:
    def __init__(self, problem_path, parent_mu, children_lambda, mutation_probability, starting_population_multipliyer):
        self.problem: tsplib95.models.StandardProblem = tsplib95.load(problem_path)
        self.parent_mu = parent_mu
        self.children_lambda = children_lambda
        self.mutation_probability = mutation_probability
        self.starting_population_size = self.parent_mu * starting_population_multipliyer

        self.best_of_generation = []

        self.fig = None
        self.ax = None

    async def init_population(self, starting_population_size):
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

    def _order_crossover_recombination_operator(self, parent1: List[int], parent2: List[int], lower_bound, upper_bound):
        proto_child = [None] * len(parent1)
        inserted = set()

        for i in range(lower_bound, upper_bound + 1):
            proto_child[i] = parent1[i]
            inserted.add(parent1[i])

        result_counter = 0

        for i in range(0, len(parent2) - 1):
            if lower_bound == upper_bound and result_counter == upper_bound:
                result_counter += 1
            elif result_counter in range(lower_bound, upper_bound):
                result_counter += upper_bound - lower_bound + 1
            if parent2[i] not in inserted:
                proto_child[result_counter] = parent2[i]
                result_counter += 1

        if proto_child[len(proto_child) - 1] is None:
            proto_child[len(proto_child) - 1] = proto_child[0]

        return proto_child

    def selection_operator(self, generation):
        survivors = []

        # TODO REMOVE DIRTY BUG FIX
        generation.pop(len(generation) - 1)

        for _ in range(self.parent_mu if self.parent_mu < len(generation) else len(generation)):
            survivors.append(heapq.heappop(generation))

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

    async def gen_new_gen(self, old_gen):
        best_parents = self.selection_operator(old_gen)
        next_gen = []

        for i in range(self.children_lambda):
            child = self.order_crossover_recombination_operator(random.choice(best_parents)[1],
                                                                random.choice(best_parents)[1])
            mutated_child = self.mutation_operator(child, self.mutation_probability)
            heapq.heappush(next_gen, (self.calc_fitness(mutated_child), mutated_child))

        for i in range(len(best_parents) - 1):
            heapq.heappush(next_gen, best_parents[i])

        for _ in range(30):
            self.gen_random_path()

        return next_gen

    async def _find_best_path(self):
        max_threads = 4
        generations = [self.init_population(self.starting_population_size) for _ in range(max_threads)]
        generations = await asyncio.gather(*generations)
        generation_counter = 0
        best_individuals_per_thread = []

        while generation_counter < 2000:
            tasks = [self.gen_new_gen(gen) for gen in generations]
            new_generations = await asyncio.gather(*tasks)

            generations = new_generations
            generation_counter += 1
            # for gen in generations:
            #     print(f"Generation {str(generation_counter)}: {str(gen)}\n")
            if generation_counter % 10 == 0:
                best_of_each_async = [sublist[0] for sublist in generations if sublist]
                best = min(best_of_each_async, key=lambda x: x[0])
                self.plot_tour(best[1], best[0], generation_counter)

        for gen in generations:
            best_individuals = heapq.nsmallest(int(self.parent_mu/max_threads), gen, key=lambda x: x[0])
            best_individuals_per_thread.extend(best_individuals)

        merged_population = heapq.nsmallest(int(self.parent_mu/max_threads), best_individuals_per_thread, key=lambda x: x[0])

        while True:
            merged_population = await self.gen_new_gen(merged_population)
            generation_counter += 1
            if generation_counter % 10 == 0:
                self.plot_tour(merged_population[0][1], merged_population[0][0], generation_counter)
            # print(f"Generation {str(generation_counter)}: {str(merged_population)}")

            # generation = self.gen_new_gen(generation)
            # generation_counter += 1
            # if generation_counter % 100 == 0:
            #     self.best_of_generation.append((generation[0][0], generation[0][1], generation_counter))
            #     self.plot_tour(self.best_of_generation[-1][1], self.best_of_generation[-1][0], self.best_of_generation[-1][2])

    async def find_best_path(self):
        await self._find_best_path()

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

        plt.pause(0.5)
