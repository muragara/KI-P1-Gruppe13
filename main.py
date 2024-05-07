import argparse

from src.Problem import Problem


def main() -> int:
    parser = handle_args()
    args = parser
    problem_path = "TestData/SymmetricTravelingSalesmanProblem/bays29.tsp"

    problem = Problem(
        problem_path=problem_path,
        parent_mu=args.parents,
        children_lambda=args.children
    )

    problem.find_best_path()


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--parents", action="store_true", help="Number of parents", default=100)
    parser.add_argument("-c", "--children", action="store_true", help="Number of children", default=200)
    return parser.parse_args()


if __name__ == '__main__':
    main()
