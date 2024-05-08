import unittest
from src.Problem import Problem

class Test_Problem(unittest.TestCase):
    def setUp(self):
        problem_path = "../TestData/SymmetricTravelingSalesmanProblem/bays29.tsp"

        self.problem = Problem(
            problem_path=problem_path,
            parent_mu=100,
            children_lambda=200
        )

    def test_calc_fitness(self):
        fitness = self.problem.calc_fitness([1, 28, 6, 12, 9, 5, 26, 29, 3, 2, 20, 10, 4, 15, 18, 17, 14, 22, 11, 19, 25, 7, 23, 27, 8, 24, 16, 13, 21, 1])
        self.assertEqual(fitness, 2020)
