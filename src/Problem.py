import tsplib95


class Problem:
    def __init__(self, problem_path, parent_mu, children_lambda):
        self.problem = tsplib95.load(problem_path)
        self.parent_mu = parent_mu
        self.children_lambda = children_lambda

    def init_population(self):
        return

    def mutation_operator(self, mutation_probability):
        return

    def recombination_operator(self):
        return

    def selection_operator(self):
        return

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

            print(min_cost)

            current = next_node
            path.append(current)
            visited.add(current)

        path.append(start)
        return path


