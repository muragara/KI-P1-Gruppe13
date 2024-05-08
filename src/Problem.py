import random
from typing import List

import tsplib95
import heapq
import matplotlib.pyplot as plt



class Problem:
    def __init__(self, problem_path, parent_mu, children_lambda):
        self.problem : tsplib95.models.StandardProblem = tsplib95.load(problem_path)
        self.parent_mu = parent_mu
        self.children_lambda = children_lambda
        self.generations = []
        self.bestOfGeneration = []
        self.counter = 0

    def init_population(self):
        initial_population = []
        for i in range(self.parent_mu * 10):
            initial_population.append(self.gen_random_path())

        self.generations.append(initial_population)

    def gen_random_path(self):
        cities = list(range(self.problem.dimension))
        random.shuffle(cities)
        cities.append(cities[0])

        heapq.heappush(self.generations, (self.calc_fitness(cities), cities))

    def mutation_operator(self, path, mutation_probability):
        res = path
        for i in range(len(res) - 1):
            if random.random() < mutation_probability:
                temp = res[i]
                random_selector = random.choice(list(range((len(res) - 1))))
                res[i] = res[random_selector]
                res[random_selector] = temp

        return res


    def order_crossover_recombination_operator(self, parent1: List[int], parent2: List[int]):
        lower_bound = random.randrange(0, len(parent1) - 1)
        upper_bound = random.randrange(lower_bound, len(parent1) - 1)
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


    def selection_operator(self):
        survivors = []

        # TODO REMOVE DIRTY BUG FIX
        self.generations.pop(len(self.generations) - 1)

        for _ in range(self.parent_mu):
            survivors.append(heapq.heappop(self.generations))

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
            fitness += self.problem.edge_weights[path[i] - 1][path[i + 1] - 1]

        return fitness

    def find_best_path(self):
        self.init_population()
        self.plot_tour(self.generations[0][1])

        while True:
            parents = self.selection_operator()
            next_gen = []

            for i in range(self.children_lambda):
                child = self.order_crossover_recombination_operator(random.choice(parents)[1], random.choice(parents)[1])
                mutated_child = self.mutation_operator(child, 0.2)
                heapq.heappush(next_gen, (self.calc_fitness(mutated_child), mutated_child))

            for i in range(len(parents) - 1):
                heapq.heappush(next_gen, parents[i])

            for _ in range(30):
                self.gen_random_path()

            self.generations = []
            self.generations = next_gen

            print("Fitness: " + str(self.generations[0][0]) + "Path:" + str(self.generations[0][1]))
            self.counter += 1

            if self.counter % 300 == 0:
                self.plot_tour(self.generations[0][1])


    def plot_tour(self, path):
        points = {node: self.problem.display_data[node] for node in self.problem.get_nodes()}

        for node in path:
            x, y = points[node + 1]
            plt.plot(x, y, 'bo')

        for i in range(len(path) - 1):
            x1, y1 = points[path[i] + 1]
            x2, y2 = points[path[i + 1] + 1]
            plt.plot([x1, x2], [y1, y2], 'b-')

        x_start, y_start = points[path[0]]
        x_end, y_end = points[path[-1]]
        plt.plot([x_end, x_start], [y_end, y_start], 'b-')

        plt.title("TSP Tour")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.grid(True)
        plt.show()





