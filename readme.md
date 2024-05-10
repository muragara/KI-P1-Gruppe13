# TH-Köln KI Praktikum 1 
## Options
```
options:
  -h, --help            show this help message and exit
  -p PARENTS, --parents PARENTS
                        Number of parents
  -c CHILDREN, --children CHILDREN
                        Number of children
  -m MUTATION, --mutation MUTATION
                        Mutation probability, is by default 1/dimension
  -s STARTING_POPULATION, --starting_population STARTING_POPULATION
                        Starting population = s * parents
  -n NEIGHBOR, --neighbor NEIGHBOR
                        Insert a path with the nearest neighbor algorithm into the startion population
  -u UPDATE, --update UPDATE
                        How often the plot is updated
  -t TSP_NAME, --tsp_name TSP_NAME
                        Name of the tsp file

```

## Example usage
```bash
python main.py -c 200 -p 100 -s 1 -n False -u 5
```
```bash
python main.py -c 200 -p 100 -s 1 -n True -u 1 -t bier127
```