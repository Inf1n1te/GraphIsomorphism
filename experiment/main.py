from enum import Enum

from experiment import graphIO as io
from experiment.algorithm import *

# graph_file = '../graphs/colorref_smallexample_6_15.grl'
# graph_file = '../graphs/torus24.grl'
# graph_file = '../graphs/trees90.grl'
graph_file = '../graphs/products72.grl'
# graph_file = '../graphs/cographs1.grl' # TODO: goes out of range, colors aren't freed or something?
# graph_file = '../graphs/bigtrees1.grl'


def iso_check(g: Graph, h: Graph):
    if prerequisites(g, h):
        i = disjoint_union(g, h, unsafe=True)
        initial_coloring(i)
        color_refine(i)
        r = isomorph_test(i)

        if r is None:
            return Result.UNDETERMINED
        elif r:
            return Result.ISOMORHP
        else:
            return Result.NOT_ISOMORPH
    else:
        return Result.DIFFERENCE_IN_EDGES_OR_VERTICES


class Result(Enum):
    ISOMORHP, NOT_ISOMORPH, DIFFERENCE_IN_EDGES_OR_VERTICES, UNDETERMINED = range(4)


def main():
    graphs = io.loadgraph(filename=graph_file, readlist=True)[0]
    isomorphisms = []
    number_of_graphs = len(graphs)
    if number_of_graphs < 2:
        print("Only 1 graph in graphlist.")
    else:
        if iso_check(graphs[0], graphs[1]) == Result.ISOMORHP:
            isomorphisms.append([0, 1])
        else:
            isomorphisms.append([0])
            isomorphisms.append([1])

        if number_of_graphs > 2:
            for i in range(2, number_of_graphs):
                for j in isomorphisms:
                    if iso_check(graphs[i], graphs[j[0]]) == Result.ISOMORHP:
                        isomorphisms[j[0]].append(i)
                        break
                isomorphisms.append([i])

    # prints isomorphisms
    for i in isomorphisms:
        if len(i) > 1:
            print(i)


if __name__ == '__main__':
    main()
