from experiment.structures.basicgraphs import Graph
from experiment.structures.doublylinkedlist import DoublyLinkedList


def initial_coloring_fast(g: Graph):
    g.queue = DoublyLinkedList()
    g.color_classes = {}  # (key, value) = (color_num, ColorClass Object)

    g.available_colors = DoublyLinkedList()  # using pop left, we can efficiently grab the lowest unused color.
    for i in range(len(g.vertices())):
        g.available_colors.append(i)

    del_colors = []  # local list to check if color has been removed already.
    queue_pointer = {}  # (color, dllnode)
    biggest_cc = (0, 0)  # (color, size)
    for v in g.vertices():
        # initial coloring
        v.colornum = v.degree()

        # update available colors list and update color class
        if v.colornum in del_colors:  # color has been seen before
            # add vertex to color class
            cc = g.color_classes[v.colornum]
            dll_node = cc.vertices.append(v)
            if len(cc.vertices) > biggest_cc[1]:  # calling len() on a dll, is O(1).
                biggest_cc = (v.colornum, len(cc.vertices))
        else:  # color hasn't been seen before.
            # update available colors
            g.available_colors.remove(v.colornum)
            del_colors.append(v.colornum)

            # create color_dict entry
            cc = ColorClass(in_queue=True, color_num=v.colornum)
            dll_node = cc.vertices.append(v)
            g.color_classes[v.colornum] = cc

            # add color to queue
            queue_node = g.queue.append(v.colornum)
            queue_pointer[v.colornum] = queue_node
        v.dll_node = dll_node
    # remove biggest color class from queue.
    queue_pointer[biggest_cc[0]].delete_self()
    g.color_classes[biggest_cc[0]].in_queue = False


def refine_fast(g: Graph):
    if hasattr(g, 'queue') and hasattr(g, 'color_classes'):
        if hasattr(g, 'available_colors'):
            while len(g.queue) > 0:
                c_color = g.queue.pop_left()
                c_class = g.color_classes[c_color]

                visited_classes = {c_color}
                for cv in c_class.vertices:
                    for c_nb in cv.nbs():
                        if c_nb.colornum in visited_classes:
                            # skip
                            pass
                        else:
                            visited_classes.update({c_nb.colornum})
                            cc_prime = g.color_classes[c_nb.colornum]
                            c_prime = cc_prime.color_num
                            if len(cc_prime.vertices) == 1:
                                continue

                            first = True
                            di_c = {}
                            local_queue = DoublyLinkedList()
                            lq_pointer = {}  # (colornum, lq_node)
                            biggest_split = ColorClass(color_num=-1)  # dummy CC
                            new_cc = None
                            for v in cc_prime.vertices:
                                nbs_in_c = 0
                                for j in v.nbs():
                                    if j.colornum == c_color:
                                        nbs_in_c += 1

                                if nbs_in_c in di_c:
                                    z = di_c[nbs_in_c]
                                    z.vertices.append(v)
                                    v.colornum = z.color_num
                                    if z.color_num != c_prime and len(z.vertices) > len(biggest_split.vertices):
                                        biggest_split = z

                                else:
                                    if first:
                                        new_color = c_prime
                                        first = False
                                    else:
                                        new_color = g.available_colors.pop_left()
                                    new_cc = ColorClass(in_queue=True, data=[v], color_num=new_color)
                                    lq_node = local_queue.append(new_color)
                                    lq_pointer[new_color] = lq_node

                                    v.colornum = new_color
                                    di_c[nbs_in_c] = new_cc
                                    g.color_classes[new_color] = new_cc

                                    if len(new_cc.vertices) > len(biggest_split.vertices):
                                        biggest_split = new_cc
                            if len(local_queue) == 1:
                                new_cc.in_queue = c_prime in g.queue
                                continue

                            else:
                                biggest_split.in_queue = False
                                lq_pointer[biggest_split.color_num].delete_self()

                            for l in local_queue:
                                g.queue.append(l)

                            if len(g.color_classes) == len(g.vertices()):
                                return


class ColorClass:
    def __init__(self, in_queue: bool = False, data=[], color_num=None):
        self.in_queue = in_queue
        self.vertices = DoublyLinkedList(data)
        self.color_num = color_num
