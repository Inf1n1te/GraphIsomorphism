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
                #print(g.queue)
                c_color = g.queue.pop_left()

                for (c_prime, cc_prime) in g.color_classes.copy().items():
                    if c_prime == c_color or len(cc_prime.vertices) == 1:
                        """
                        a class doesn't refine itself.
                        and a class of 1 node can't be refined.
                        """
                        continue
                    else:
                        """
                        intersection of di and c', the new color classes after refine of c_prime.
                        (#_of_nbs_in_c, Colorclass)
                        """

                        c_prime_in_queue = c_prime in g.queue
                        first = True
                        di_c = {}
                        local_queue = DoublyLinkedList()
                        lq_pointer = {} # (colornum, lq_node)
                        biggest_split = ColorClass(color_num=-1) # dummy CC
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
                                    if c_prime_in_queue:
                                        new_cc = ColorClass(in_queue=False, data=[v], color_num=new_color)
                                    else:
                                        new_cc = ColorClass(in_queue=True, data=[v], color_num=new_color)
                                        lq_node = local_queue.append(new_color)
                                        lq_pointer[new_color] = lq_node
                                        biggest_split = new_cc

                                else:
                                    new_color = g.available_colors.pop_left()
                                    new_cc = ColorClass(in_queue=True, data=[v], color_num=new_color)
                                    lq_node = local_queue.append(new_color)
                                    lq_pointer[new_color] = lq_node

                                v.colornum = new_color
                                di_c[nbs_in_c] = new_cc
                                g.color_classes[new_color] = new_cc

                                if new_color != c_prime and len(new_cc.vertices) > len(biggest_split.vertices):
                                    biggest_split = new_cc
                                first = False

                        if len(local_queue) == 0:
                            continue
                        else: # elif len(local_queue) > 1: # if only 1 in local queue at this point, we must force this on queue
                            biggest_split.in_queue = False
                            lq_pointer[biggest_split.color_num].delete_self()

                        for l in local_queue:
                            g.queue.append(l)


class ColorClass:
    def __init__(self, in_queue: bool = False, data=[], color_num=None):
        self.in_queue = in_queue
        self.vertices = DoublyLinkedList(data)
        self.color_num = color_num


def refine_fast2(g: Graph):
    if hasattr(g, 'queue') and hasattr(g, 'color_classes'):
        if hasattr(g, 'available_colors'):
            while len(g.queue) > 0:
                c_color = g.queue.pop_left()
                c = g.color_classes[c_color]

                for (c_prime, cc_prime) in g.color_classes.copy().items():
                    if c_prime == c_color or len(cc_prime.vertices) < 2:  # a class doesn't refine itself.
                        continue
                    else:
                        # intersection of di and c', the new color classes after refine of c_prime. (#_of_nbs_in_c,
                        # vertices)
                        di_c = {}
                        for v in cc_prime.vertices:
                            nbs_in_c = 0
                            for j in v.nbs():
                                if j in c.vertices:
                                    nbs_in_c += 1

                            if nbs_in_c in di_c:
                                di_c[nbs_in_c].vertices.append(v)
                            else:
                                di_c[nbs_in_c] = ColorClass(in_queue=True, data=[v])

                        # Decide which splits go on the queue
                        local_queue = DoublyLinkedList()
                        biggest_split = (0, None, None)  # (size, lq_node, cc)
                        first = True

                        di_c_partitions = len(di_c)

                        if di_c_partitions > 1:
                            for (x, y) in di_c.items():
                                if len(y.vertices) == 1:
                                    # TODO dont push on queue when this partition has only one vertex
                                    pass
                                if first:  # keep this color, assign (split) vertexlist.
                                    first = False
                                    new_color = c_prime
                                    if not g.color_classes[new_color].in_queue:
                                        lq_node = local_queue.append(new_color)
                                        if len(y.vertices) > biggest_split[0]:
                                            biggest_split = (len(y.vertices), lq_node, y)
                                else:
                                    new_color = g.available_colors.pop_left()
                                    lq_node = local_queue.append(new_color)
                                    if len(y.vertices) > biggest_split[0]:
                                        biggest_split = (len(y.vertices), lq_node, y)
                                g.color_classes[new_color] = y

                            # deletes biggest split from queue
                            # len(local_queue) is only 1 when len(di_c) = 2 and i/c_prime was already on the queue.
                            # Thus we must force the second element on the queue for refinement.
                            if len(local_queue) > 1 and biggest_split[1] is not None:
                                biggest_split[1].delete_self()
                                biggest_split[2].in_queue = False

                            # add local queue to graph queue
                            for l in local_queue:
                                g.queue.append(l)
