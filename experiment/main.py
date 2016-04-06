import os
import time

from experiment.algorithms.fastrefine import *
from experiment.algorithms.slowrefine import *
from experiment.io import graphIO as io

tp5 = 'testinstances/threepaths5.gr'
tp80 = 'testinstances/threepaths80.gr'
tp320 = 'testinstances/threepaths320.gr'
tp640 = 'testinstances/threepaths640.gr'
tp1280 = 'testinstances/threepaths1280.gr'
tp5120 = 'testinstances/threepaths5120.gr'
tp10240 = 'testinstances/threepaths10240.gr'

graph_file_list = [tp5, tp80, tp320, tp640, tp1280, tp5120, tp10240]
SLOW = False  # Should we run color refinement using the slow algorithm


def experiment():
    for graph_file in graph_file_list:
        print("Graph: " + str(os.path.basename(graph_file)))
        print("Type | Time initial | Time refinement | Color classes")
        graphs = io.loadgraph(filename=graph_file, readlist=True)[0]
        g = graphs[0]

        if SLOW:
            print("******* Copying Graph *******", end="")
            h = copy.copy(g)

            print("\rSlow | <COMPUTING> | <COMPUTING> | <COMPUTING>", end="")
            h1 = time.time()
            initial_coloring(h)
            h2 = time.time()
            hi = h2 - h1
            print("\rSlow | " + str(hi) + " | <COMPUTING> | <COMPUTING>", end="")

            color_refine(h)
            h3 = time.time()
            hr = h3 - h2
            print("\rSlow | " + str(hi) + " | " + str(hr) + " | " + str(len(h.color_dict)))

        print("Fast | <COMPUTING> | <COMPUTING> | <COMPUTING>", end="")
        g1 = time.time()
        initial_coloring_fast(g)
        g2 = time.time()
        gi = g2 - g1
        print("\rFast | " + str(gi) + " | <COMPUTING> | <COMPUTING>", end="")

        refine_fast(g)
        g3 = time.time()
        gr = g3 - g2
        print("\rFast | " + str(gi) + " | " + str(gr) + " | " + str(len(g.color_classes)))

        print("\n" + str("-" * 50) + "\n")


if __name__ == '__main__':
    experiment()
