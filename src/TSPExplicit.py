from .TSP import TSP

class TSPExplicit(TSP):
    def __init__(self, name, dimension):
        super().__init__(name, dimension, 'EXPLICIT')

    # TODO does not work
    def calculate_distances(self, weights):
        index = 0
        for i in range(self.dimension):
            for j in range(i + 1, self.dimension):
                self.add_edge_weight(i, j, weights[index])
                index += 1