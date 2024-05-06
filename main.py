import tsplib95
import matplotlib.pyplot as plt

def main() -> int:
    problem = tsplib95.load("TestData/SymmetricTravelingSalesmanProblem/bays29.tsp")
    plot_tour(problem)
def plot_tour(problem):
    points = {node: problem.display_data[node] for node in problem.get_nodes()}
    for node, (x, y) in points.items():
        plt.plot(x, y, 'bo')

    plt.title("TSP Tour")
    plt.show()

if __name__ == '__main__':
    main()
