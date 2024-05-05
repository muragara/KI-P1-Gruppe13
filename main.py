import src.TSPExplicit as tsp

def main() -> int:
    weights = [97, 205, 139, 86, 60]  
    tsp_explicit = tsp.TSPExplicit('bayg29', 29)
    tsp_explicit.calculate_distances(weights)
    print(tsp_explicit.get_distance(0, 1)) 

if __name__ == '__main__':
    main()