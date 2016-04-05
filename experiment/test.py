from timeit import *

from experiment.algorithm import color_refine
from experiment.graphIO import loadgraph

threepaths = []


def main():
    path = '../graphs/threepaths'
    threepaths.append(loadgraph(path + '5.gr'))
    threepaths.append(loadgraph(path + '10.gr'))
    threepaths.append(loadgraph(path + '20.gr'))
    threepaths.append(loadgraph(path + '40.gr'))
    threepaths.append(loadgraph(path + '80.gr'))
    threepaths.append(loadgraph(path + '160.gr'))
    threepaths.append(loadgraph(path + '320.gr'))
    threepaths.append(loadgraph(path + '640.gr'))
    threepaths.append(loadgraph(path + '1280.gr'))
    threepaths.append(loadgraph(path + '2560.gr'))
    threepaths.append(loadgraph(path + '5120.gr'))
    threepaths.append(loadgraph(path + '10240.gr'))
    print(min(Timer(t0).repeat(3, 1)))
    print(min(Timer(t1).repeat(3, 1)))
    print(min(Timer(t2).repeat(3, 1)))
    print(min(Timer(t3).repeat(3, 1)))
    print(min(Timer(t4).repeat(3, 1)))
    print(min(Timer(t5).repeat(3, 1)))
    print(min(Timer(t6).repeat(3, 1)))
    print(min(Timer(t7).repeat(3, 1)))
    print(min(Timer(t8).repeat(3, 1)))
    print(min(Timer(t9).repeat(3, 1)))
    print(min(Timer(t10).repeat(3, 1)))
    print(min(Timer(t11).repeat(3, 1)))


def t0():
    color_refine(threepaths[0])


def t1():
    color_refine(threepaths[1])


def t2():
    color_refine(threepaths[2])


def t3():
    color_refine(threepaths[3])


def t4():
    color_refine(threepaths[4])


def t5():
    color_refine(threepaths[5])


def t6():
    color_refine(threepaths[6])


def t7():
    color_refine(threepaths[7])


def t8():
    color_refine(threepaths[8])


def t9():
    color_refine(threepaths[9])


def t10():
    color_refine(threepaths[10])


def t11():
    color_refine(threepaths[11])


main()