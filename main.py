import argparse

from src.Problem import Problem


def main() -> int:
    parser = handle_args()
    args = parser
    problem_path = f"TestData/SymmetricTravelingSalesmanProblem/{args.tsp_name}.tsp"

    problem = Problem(
        problem_path=problem_path,
        parent_mu=args.parents,
        children_lambda=args.children,
        mutation_probability=args.mutation,
        starting_population_multipliyer=args.starting_population,
        cheat=parse_bool(args.neighbor),
        plot_update=args.update
    )

    problem.find_best_path()


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--parents", type=int, help="Number of parents", default=100)
    parser.add_argument("-c", "--children", type=int, help="Number of children", default=200)
    parser.add_argument("-m", "--mutation", type=float, help="Mutation probability, is by default 1/dimension", default=None)
    parser.add_argument("-s", "--starting_population", type=int, help="Starting population = s * parents", default=10)
    parser.add_argument("-n", "--neighbor", type=str, help="Insert a path with the nearest neighbor algorithm into the startion population", default=False)
    parser.add_argument("-u", "--update", type=int, help="How often the plot is updated", default=10)
    parser.add_argument("-t", "--tsp_name", type=str, help="Name of the tsp file", default="bays29")
    return parser.parse_args()

def parse_bool(b):
    if b == "True":
        return True
    elif b == "False":
        return False
    else:
        raise ValueError(f"Unknown bool value {b}")


if __name__ == '__main__':
    main()
