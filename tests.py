from timeit import *

from colorRefinement import *
from graphIO import loadgraph

threepaths = []


def main():
    path = 'threepaths/threepaths'
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
    # print(Timer(t0).repeat(3, 1))
    # print(Timer(t1).repeat(3, 1))
    # print(Timer(t2).repeat(3, 1))
    # print(Timer(t3).repeat(3, 1))
    # print(Timer(t4).repeat(3, 1))
    # print(Timer(t5).repeat(3, 1))
    # print(Timer(t6).repeat(3, 1))
    # print(Timer(t7).repeat(3, 1))
    # print(Timer(t8).repeat(3, 1))
    # print(Timer(t9).repeat(3, 1))
    # print(Timer(t10).repeat(3, 1))
    # print(Timer(t11).repeat(3, 1))


def t0():
    fastrefine(threepaths[0])


def t1():
    fastrefine(threepaths[1])


def t2():
    fastrefine(threepaths[2])


def t3():
    fastrefine(threepaths[3])


def t4():
    fastrefine(threepaths[4])


def t5():
    fastrefine(threepaths[5])


def t6():
    fastrefine(threepaths[6])


def t7():
    fastrefine(threepaths[7])


def t8():
    fastrefine(threepaths[8])


def t9():
    fastrefine(threepaths[9])


def t10():
    fastrefine(threepaths[10])


def t11():
    fastrefine(threepaths[11])


main()
