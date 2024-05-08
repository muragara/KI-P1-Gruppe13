import argparse
import asyncio

from src.Problem import Problem


async def main() -> int:
    parser = handle_args()
    args = parser
    problem_path = "TestData/SymmetricTravelingSalesmanProblem/bays29.tsp"
    # problem_path = "./TestData/AsymmetricTravelingSalesmanProblem/rbg443.atsp"
    # problem_path = "TestData/SymmetricTravelingSalesmanProblem/a280.tsp"
    # problem_path = "TestData/SymmetricTravelingSalesmanProblem/bier127.tsp"
    # problem_path = "TestData/SymmetricTravelingSalesmanProblem/rl1304.tsp"

    problem = Problem(
        problem_path=problem_path,
        parent_mu=args.parents,
        children_lambda=args.children,
        mutation_probability=args.mutation,
        starting_population_multipliyer=args.starting_population
    )

    await problem.find_best_path()


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--parents", type=int, help="Number of parents", default=100)
    parser.add_argument("-c", "--children", type=int, help="Number of children", default=200)
    parser.add_argument("-m", "--mutation", type=float, help="Mutation probability", default=0.2)
    parser.add_argument("-s", "--starting_population", type=int, help="Starting population = s * parents", default=10)
    return parser.parse_args()


if __name__ == '__main__':
    asyncio.run(main())
