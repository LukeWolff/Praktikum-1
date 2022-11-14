import tsplib95

import evolution

tspFile = "d15112.tsp"


def main():
    # Load the tsp file data and creates the graph
    # Data representation node/point in graph and x and y coordinate
    problem = evolution.Population(10)
    problem.evolutionary_algorithm(10000, 1, 4)
    # 10 POP 4000 , 1, 2
    # 100 POP 4000, 1, 10

if __name__ == '__main__':
    main()
