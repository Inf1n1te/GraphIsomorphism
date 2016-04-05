import copy

from experiment.structures.basicgraphs import *


def initial_coloring(g: Graph):
    g.color_dict = {}
    for v in g.vertices():
        v.colornum = v.degree()
    for v in g.vertices():
        if v.colornum not in g.color_dict:
            g.color_dict[v.colornum] = (v.degree(), create_nbs_dict(v))
    return


def create_nbs_dict(v: Vertex, update: bool = False) -> {}:
    """
    Creates a dictionary holding the colors of the neighbourhood of vertex v, and their number of appearance.
    :param v:
    :param update:
    :return:
    """
    nbs_dict = {}
    for nb in v.nbs():
        c = nb.colornum
        if update and hasattr(nb, 'new_colornum'):
            c = nb.new_colornum
        if c in nbs_dict:
            nbs_dict[c] += 1
        else:
            nbs_dict[c] = 1
    return nbs_dict


def new_color(g: Graph):
    if hasattr(g, "color_dict"):
        c = 0
        while c in g.color_dict:
            c += 1
        return c
    else:
        raise GraphError("Graph has no color dictionary")


def color_refine(g: Graph):
    # color_dict{key, value} = {colornum, (degree, nbs_dict)}
    if hasattr(g, "color_dict"):
        changed = True
        while changed:
            changed = False
            for v in g.vertices():
                nbs_dict = create_nbs_dict(v)
                if g.color_dict[v.colornum][1] == nbs_dict:
                    # dont update, as the nbs are equivalent
                    pass
                else:
                    existing_config = False
                    for c, (d, n) in g.color_dict.items():
                        if d == v.degree() and n == nbs_dict:
                            # already assigned this configuration a new color
                            v.new_colornum = c
                            existing_config = True
                            break
                    if not existing_config:
                        # This configuration is not yet known, assign a new color
                        c = new_color(g)
                        v.new_colornum = c
                        g.color_dict[c] = (v.degree(), nbs_dict)

            for v in g.vertices():
                # update colors
                if hasattr(v, 'new_colornum'):
                    v.colornum = v.new_colornum
                    del v.new_colornum
                    changed = True
                # update color_dict
                g.color_dict[v.colornum] = (v.degree(), create_nbs_dict(v, True))

        return
    else:
        raise GraphError("Graph has no color dictionary")


def branching(g: Graph):
    possible = []
    g.colors_freq = {}
    for v in g.vertices():
        if v.colornum in g.colors_freq:
            g.colors_freq[v.colornum].append(v)

            if len(g.colors_freq[v.colornum]) >= 4:
                if v.colornum not in possible:
                    possible.append(v.colornum)
        else:
            g.colors_freq[v.colornum] = [v]

    if possible:  # empty list is false
        for c in possible:
            cmpl = g.number_of_vertices() / 2
            branches = []  # label numbers of possible branches
            branch_label = None
            for w in g.colors_freq[c]:
                l = w.label()
                if l < cmpl:
                    branches.append(l)
                else:
                    branch_label = l

            branch_color = new_color(g)
            for b in branches:
                h = copy.deepcopy(g)
                bv = h[branch_label]
                bv.colornum = branch_color
                h[b].colornum = branch_color
                h.color_dict[branch_color] = (bv.degree(), create_nbs_dict(bv))
                color_refine(h)
                return isomorph_test(h)


def isomorph_test(g: Graph):
    colors0 = [0] * g.number_of_vertices()
    colors1 = [0] * g.number_of_vertices()
    cmpl = g.number_of_vertices() / 2
    for i in g.vertices():
        if i.label() < cmpl:
            colors0[i.colornum] += 1
        else:
            colors1[i.colornum] += 1
    if colors0 == colors1:
        if max(colors0) == 1:
            return True
        else:
            return branching(g)
    else:
        return False


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
