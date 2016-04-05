class _DoublyNode:
    def __init__(self, data, prev, next_):
        self.data = data
        self.prev = prev
        self.next = next_
        pass

    pass


class DoublyLinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        pass

    def append(self, data):
        new_node = _DoublyNode(data, None, None)
        if self._head is None:
            # empty list
            self._head = self._tail = new_node
        else:
            # link nodes together
            self._tail.next = new_node
            new_node.prev = self._tail
            # update tail
            self._tail = new_node
        pass

    def remove(self, data, all_instances: bool = False):
        pointer = self._head
        p = None
        while pointer is not None:
            if pointer.data == data:
                # first element is head
                if pointer.prev is None:
                    self._head = pointer.next
                    self._head.prev = None
                    p = pointer.next
                    pointer.next = None
                elif pointer.next is None:
                    self._tail = pointer.prev
                    self._tail.next = None
                    pointer.prev = None
                else:
                    pointer.prev.next = pointer.next
                    pointer.next.prev = pointer.prev
                if not all_instances:
                    break
            if p is not None:
                pointer = p
                p = None
            else:
                pointer = pointer.next
        pass

    def __repr__(self):
        pointer = self._head
        if pointer is None:
            return "[]"
        r = "[" + str(pointer.data)
        pointer = pointer.next
        while pointer is not None:
            r += ", "
            r += str(pointer.data)
            pointer = pointer.next
        return r + "]"
