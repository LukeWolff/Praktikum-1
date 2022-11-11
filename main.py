import evolution

tspFile = "d15112.tsp"

def main():

    #Load the tsp file data and creates the graph
    problem = evolution.Population(100)
    problem.evolutionary_algorithm(100)


if __name__ == '__main__':
    main()