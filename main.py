import tsplib95

import evolution

tspFile = "d15112.tsp"

def main():
    # Load the tsp file data and creates the graph
    # Data representation node/point in graph and x and y coordinate
    problem = evolution.Population(2)
    problem.evolutionary_algorithm(1)


if __name__ == '__main__':
    main()