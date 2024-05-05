from abc import ABC, abstractmethod

class TSP(ABC):
    def __init__(self, name, dimension, edge_weight_type):
        self.name = name
        self.dimension = dimension
        self.edge_weight_type = edge_weight_type
        self.distances = [[0]*dimension for _ in range(dimension)]
    
    @abstractmethod
    def calculate_distances(self):
        pass

    def add_edge_weight(self, i, j, weight):
        self.distances[i][j] = weight
        self.distances[j][i] = weight

    def get_distance(self, i, j):
        return self.distances[i][j]
