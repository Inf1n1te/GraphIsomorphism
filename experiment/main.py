from experiment import graphIO as io
from experiment.algorithm import *

if __name__ == '__main__':
    graphs = io.loadgraph(filename='../graphs/colorref_smallexample_6_15.grl', readlist=True)[0]
    number_of_graphs = len(graphs)
    for i in range(number_of_graphs):
        for j in range(i, number_of_graphs):
            if i == j:
                continue
            g = disjoint_union(graphs[i], graphs[j])
            initial_coloring(g)
            color_refine(g)
            r = isomorph_test(g)

            if r is None:
                print("Graphs %d & %d | undetermined" % (i, j))
            elif r:
                print("Graphs %d & %d | isomorph" % (i, j))
            else:
                print("Graphs %d & %d | not isomorph" % (i, j))
    pass
