from experiment.basicgraphs import *


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


def isomorph_test(g: Graph):
    colors1 = [0] * g.number_of_vertices()
    colors2 = [0] * g.number_of_vertices()
    cmpl = g.number_of_vertices() / 2
    for i in g.vertices():
        if i._label < cmpl:
            colors1[i.colornum] += 1
        else:
            colors2[i.colornum] += 1
    if colors1 == colors2:
        if max(colors1) == 1:
            return True
        else:
            # Need branching
            return None
    else:
        return False


def disjoint_union(g: Graph, h: Graph) -> Graph:
    # Stolen from blackboard.
    vertex_map = {}
    r = Graph()
    for v in g.vertices() + h.vertices():
        vertex_map[v] = r.add_vertex()
    for e in g.edges() + h.edges():
        r.add_edge(vertex_map[e.tail()], vertex_map[e.head()])
    return r
