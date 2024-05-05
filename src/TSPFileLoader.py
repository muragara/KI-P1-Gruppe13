import re
import TSPExplicit as TSPExplicit

class TSPFileLoader:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        with open(self.filename, 'r') as file:
            content = file.read()

        for line in content.split('\n'):
            if line.startswith('NAME :'):
                name = line.split()[1]
            elif line.startswith('COMMENT :'):
                comment = line.split()[1]
            elif line.startswith('TYPE :'):
                tspType = line.split()[1]
            elif line.startswith('DIMENSION :'):
                dimension = int(line.split()[1])
            elif line.startswith('EDGE_WEIGHT_TYPE :'):
                edgeWeightType = line.split()[1]
            elif line.startswith('EDGE_WEIGHT_FORMAT'):
                edgeWeightFormat = line.split()[1]
            elif line.startswith('DISPLAY_DATA_TYPE'):
                displayDataType = line.split()[1]
            elif line.startswith('EDGE_WEIGHT_SECTION'):
                break


        if edgeWeightType == 'EXPLICIT':
            tsp_instance = TSPExplicit(name, dimension)
            if(edgeWeightFormat == "TWOD_DISPLAY"):
                dimensionString = re.search('EDGE_WEIGHT_SECTION(.*)DISPLAY_DATA_SECTION', content)
            elif edgeWeightFormat == "FULL_MATRIX":
                dimensionString = re.search('EDGE_WEIGHT_SECTION(.*)EOF', content)
            weights = []
            for line in dimensionString.group(1).split('\n'):
                if line == '':
                    continue
                weights.extend([int(x) for x in line.split()])
            tsp_instance.calculate_distances(weights)

        if tsp_instance is None:
            raise ValueError('Unsupported EDGE_WEIGHT_TYPE')

        return tsp_instance

