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
        self.assertEqual(2020, fitness)

    def test_recombination_1(self):
        lower_bound = 2
        upper_bound = 5
        parent_1 = [1,2,3,4,5,6,7,8,9,1]
        parent_2 = [5,7,4,9,1,3,6,2,8,5]
        child = [7,9,3,4,5,6,1,2,8,7]
        res = self.problem._order_crossover_recombination_operator(parent_1, parent_2, lower_bound, upper_bound)

        self.assertEqual(child, res)

    def test_recombination_2(self):
        lower_bound = 5
        upper_bound = 5
        parent_1 = [1,2,3,4,5,6,7,8,9,1]
        parent_2 = [5,7,4,9,1,3,6,2,8,5]
        child = [5,7,4,9,1,6,3,2,8,5]
        res = self.problem._order_crossover_recombination_operator(parent_1, parent_2, lower_bound, upper_bound)

        self.assertEqual(child, res)

    def test_recombination_3(self):
            lower_bound = 0
            upper_bound = 0
            parent_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
            parent_2 = [5, 7, 4, 9, 1, 3, 6, 2, 8, 5]
            child = [1, 5, 7, 4, 9, 3, 6, 2, 8, 1]
            res = self.problem._order_crossover_recombination_operator(parent_1, parent_2, lower_bound, upper_bound)

            self.assertEqual(child, res)

    def test_recombination_4(self):
            lower_bound = 0
            upper_bound = 9
            parent_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
            parent_2 = [5, 7, 4, 9, 1, 3, 6, 2, 8, 5]
            child = parent_1
            res = self.problem._order_crossover_recombination_operator(parent_1, parent_2, lower_bound,
                                                                       upper_bound)

            self.assertEqual(child, res)
