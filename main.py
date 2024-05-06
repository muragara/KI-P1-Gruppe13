import argparse

import matplotlib.pyplot as plt
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

    print(problem.nearest_neighbors(22))
    plot_tour(problem.problem, problem.nearest_neighbors(5))


def plot_tour(problem, path):
    points = {node: problem.display_data[node] for node in problem.get_nodes()}

    for node in path:
        x, y = points[node+1]
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


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--parents", action="store_true", help="Number of parents", default=10)
    parser.add_argument("-c", "--children", action="store_true", help="Number of children", default=20)
    return parser.parse_args()


if __name__ == '__main__':
    main()
