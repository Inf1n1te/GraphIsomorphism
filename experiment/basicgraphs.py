"""
This is a module for working with *undirected* graphs (simple graphs or multigraphs).

It contains three classes: vertex, edge and graph. 

The interface of these classes is extensive and allows programming all kinds of graph algorithms.

However, the data structure used is quite basic and inefficient: a graph object stores only a vertex list and an edge
list, and methods such as adjacency testing / finding neighbors of a vertex require going through the entire edge list!
"""
# version: 29-01-2015, Paul Bonsma


unsafe = False


# Set to True for faster, but unsafe listing of all vertices and edges.

class GraphError(Exception):
    def __init__(self, message):
        self.mess = message

    def __str__(self):
        return self.mess


class Vertex:
    """
    Vertex objects have an attribute <_graph> pointing to the graph they are part of,
    and an attribute <_label> which can be anything: it is not used for any methods,
    except for __repr__.
    """

    def __init__(self, graph, label=0):
        """
        Creates a vertex, part of <graph>, with optional label <label>.
        (Labels of different vertices may be chosen the same; this does
        not influence correctness of the methods, but will make the string
        representation of the graph ambiguous.)
        """
        self._graph = graph
        self._label = label
        self._incidence_list = []
        self._degree = 0

    def __repr__(self):
        if hasattr(self, "colornum"):
            return"(" + str(self._label) + ", c=" + str(self.colornum) + ")"
        else:
            return str(self._label)

    def adjacent(self, other):
        """
        Returns True iff vertex <self> is adjacent to <other> vertex.
        """
        return self._graph.adjacent(self, other)

    def incidence_list(self):
        """
        Returns the list of edges incident with vertex <self>.
        """
        return self._incidence_list

    def nbs(self):
        """
        Returns the list of neighbors of vertex <self>.
        In case of parallel edges: duplicates are not removed from this list!
        """
        nbl = []
        for e in self.incidence_list():
            nbl.append(e.other_end(self))
        return nbl

    def degree(self) -> int:
        """
        Returns the degree of vertex <self>.
        """
        return self._degree

    def add_nb(self, e):
        self._incidence_list.append(e)
        self._degree += 1





class Edge:
    """
    Edges have attributes <_tail> and <_head> which point to the end vertices
    (vertex objects). The order of these is arbitrary (undirected edges).
    """

    def __init__(self, tail, head):
        """
        Creates an edge between vertices <tail> and <head>.
        """
        # tail and head must be vertex objects.
        if not tail._graph == head._graph:
            raise GraphError(
                'Can only add edges between vertices of the same graph')
        self._tail = tail
        self._head = head

    def __repr__(self):
        return '(' + str(self._tail) + ',' + str(self._head) + ')'

    def tail(self) -> Vertex:
        return self._tail

    def head(self) -> Vertex:
        return self._head

    def other_end(self, one_end: Vertex) -> Vertex:
        """
        Given one end vertex <one_end> of the edge <self>, this returns
        the other end vertex of <self>.
        """
        # <oneend> must be either the head or the tail of this edge.
        if self._tail == one_end:
            return self._head
        elif self._head == one_end:
            return self._tail
        raise GraphError(
            'edge.otherend(oneend): oneend must be head or tail of edge')

    def incident(self, vertex: Vertex) -> bool:
        """
        Returns True iff the edge <self> is incident with the
        vertex <vertex>.
        """
        return self._tail == vertex or self._head == vertex


class Graph:
    """
    A graph object has as main attributes:
     <_V>: the list of its vertices
     <_E>: the list of its edges
    In addition:
     <_simple> is True iff the graph must stay simple (used when trying to add edges)
     <_directed> is False for now (feel free to write a directed variant of this
         module)
     <_nextlabel> is used to assign default labels to vertices.
    """

    def __init__(self, n: int = 0, simple: bool = False):
        """
        Creates a graph.
        Optional argument <n>: number of vertices.
        Optional argument <simple>: indicates whether the graph should stay simple.
        """
        self._vertices = []
        self._edges = []
        self._directed = False
        self._number_of_vertices = 0
        self._number_of_edges = 0
        # may be changed later for a more general version that can also
        # handle directed graphs.
        self._simple = simple
        self._next_label = 0
        for i in range(n):
            self.add_vertex()

    def __repr__(self):
        return 'V=' + str(self._vertices) + '\nE=' + str(self._edges)

    def vertices(self) -> [Vertex]:
        """
        Returns the list of vertices of the graph.
        """
        if unsafe:  # but fast
            return self._vertices
        else:
            return self._vertices[:]  # return a *copy* of this list

    def edges(self) -> [Edge]:
        """
        Returns the list of edges of the graph.
        """
        if unsafe:  # but fast
            return self._edges
        else:
            return self._edges[:]  # return a *copy* of this list

    def __getitem__(self, i):
        """
        Returns the <i>th vertex of the graph -- as given in the vertex list;
        this is not related to the vertex labels.
        """
        return self._vertices[i]

    def add_vertex(self, label=-1) -> Vertex:
        """
        Add a vertex to the graph.
        Optional argument: a vertex label (arbitrary)
        """
        if label == -1:
            label = self._next_label
            self._next_label += 1
        u = Vertex(self, label)
        self._vertices.append(u)
        self._number_of_vertices += 1
        return u

    def add_edge(self, tail: Vertex, head: Vertex) -> Edge:
        """
        Add an edge to the graph between <tail> and <head>.
        Includes some checks in case the graph should stay simple.
        """
        if self._simple:
            if tail == head:
                raise GraphError('No loops allowed in simple graphs')
            for e in self._edges:
                if e._tail == tail and e._head == head:
                    raise GraphError(
                        'No multiedges allowed in simple graphs')
                if not self._directed:
                    if e._tail == head and e._head == tail:
                        raise GraphError(
                            'No multiedges allowed in simple graphs')
        if not (tail._graph == self and head._graph == self):
            raise GraphError(
                'Edges of a graph G must be between vertices of G')
        e = Edge(tail, head)
        tail.add_nb(e)
        head.add_nb(e)
        self._edges.append(e)
        self._number_of_edges += 1
        return e

    def find_edge(self, u: Vertex, v: Vertex) -> Edge or None:
        """
        If <u> and <v> are adjacent, this returns an edge between them.
        (Arbitrary in the case of multigraphs.)
        Otherwise this returns <None>.
        """
        for e in self._edges:
            if (e._tail == u and e._head == v) or (e._tail == v and e._head == u):
                return e
        return None

    def adjacent(self, u: Vertex, v: Vertex) -> bool:
        """
        Returns True iff vertices <u> and <v> are adjacent.
        """
        return self.find_edge(u, v) is not None

    def is_directed(self) -> bool:
        """
        Returns False, because for now these graphs are always undirected.
        """
        return self._directed

    def number_of_vertices(self):
        return self._number_of_vertices

    def number_of_edges(self):
        return self.number_of_edges
