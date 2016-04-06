import sys
import time
from enum import Enum

from experiment.fastrefine import *
from experiment.graphutil import prerequisites, disjoint_union
from experiment.io import graphIO as io
from experiment.slowrefine import *

# graph_file = '../graphs/colorref_smallexample_6_15.grl'
# graph_file = '../graphs/colorref_smallexample_2_49.grl'


# graph_file = '../graphs/colorref_largeexample_4_1026.grl'
# graph_file = '../graphs/torus144.grl'
# graph_file = '../graphs/trees90.grl'
# graph_file = '../graphs/products72.grl'


# graph_file = '../graphs/cographs1.grl' # TODO: goes out of range, colors aren't freed or something?
# graph_file = '../graphs/bigtrees1.grl'
# graph_file = '../graphs/wheelstar12.grl'
graph_file = '../graphs/threepaths640.gr'


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


def slow():
    graphs = io.loadgraph(filename=graph_file, readlist=True)[0]
    isomorphisms = []
    number_of_graphs = len(graphs)
    print("Number of graphs: " + str(number_of_graphs))
    if number_of_graphs > 1:
        if iso_check(graphs[0], graphs[1]) == Result.ISOMORHP:
            isomorphisms.append([0, 1])
        else:
            isomorphisms.append([0])
            isomorphisms.append([1])

        if number_of_graphs > 2:
            for i in range(2, number_of_graphs):
                j = 0
                iso = False
                while j < len(isomorphisms):
                    iso = Result.ISOMORHP == iso_check(graphs[i], graphs[isomorphisms[j][0]])
                    if iso:
                        isomorphisms[j].append(i)
                        break
                    j += 1
                if not iso:
                    isomorphisms.append([i])

    for i in isomorphisms:
        if len(i) > 1:
            print(i)


def fast():
    graphs = io.loadgraph(filename=graph_file, readlist=True)[0]
    """
    for i in range(0, len(graphs)):
        for j in range(i + 1, len(graphs)):
    """
    # g = disjoint_union(graphs[0], graphs[1], unsafe=True)
    g = graphs[0]
    h = copy.copy(g)
    f = copy.copy(g)

    h1 = time.time()
    initial_coloring(h)
    h2 = time.time()
    color_refine(h)
    h3 = time.time()

    hi = h2 - h1
    hr = h3 - h2
    print("Slow: " + str(hi) + " | " + str(hr))
    print(len(h.color_dict))

    g1 = time.time()
    initial_coloring_fast(g)
    g2 = time.time()
    refine_fast(g)
    g3 = time.time()

    gi = g2 - g1
    gr = g3 - g2

    print("Fast: " + str(gi) + " | " + str(gr))
    print(len(g.color_classes))

    f1 = time.time()
    initial_coloring(f)
    f2 = time.time()
    color_refine(f)
    f3 = time.time()

    fi = f2 - f1
    fr = f3 - f2
    print("Fast2: " + str(fi) + " | " + str(fr))
    print(len(f.color_classes))


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    fast()
