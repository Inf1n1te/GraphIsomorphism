from experiment.structures.basicgraphs import Graph


def prerequisites(g: Graph, h: Graph) -> bool:
    return len(g.vertices()) == len(h.vertices()) and len(g.edges()) == len(h.edges())


def disjoint_union(g: Graph, h: Graph, unsafe: bool = False) -> Graph:
    # Stolen from blackboard.
    vertex_map = {}
    r = Graph(unsafe=unsafe)
    for v in g.vertices() + h.vertices():
        vertex_map[v] = r.add_vertex()
    for e in g.edges() + h.edges():
        r.add_edge(vertex_map[e.tail()], vertex_map[e.head()])
    return r