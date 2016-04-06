class DoublyNode:
    def __init__(self, data, dll, prev=None, next_=None):
        self._dll = dll
        self.data = data
        self.prev = prev
        self.next = next_
        pass

    def delete_self(self):
        is_head = self == self._dll._head
        is_tail = self == self._dll._tail


        if is_head and is_tail:
            self._dll._head = None
            self._dll._tail = None
        elif is_head:
            self.next.prev = None
            self._dll._head = self.next
            self.next = None
        elif is_tail:
            self.prev.next = None
            self._dll._tail = self.prev
            self.prev = None
        else:
            self.prev.next = self.next
            self.next.prev = self.prev

        self._dll._len -= 1  # ugly but efficient.
        pass

    def get_dll(self):
        return self._dll

    pass


class DoublyLinkedList:
    def __init__(self, data : [] = None):
        self._head = None
        self._tail = None
        self._len = 0
        self._current = self._head

        if data is not None:
            for i in data:
                self.append(i)
        pass

    def __iter__(self):
        self._current = self._head
        return self

    def __next__(self):
        if self._current is None:
            self._current = self._head
            raise StopIteration
        else:
            r = self._current
            self._current = self._current.next
            return r.data

    def append(self, data):
        new_node = DoublyNode(data, self)
        self._len += 1
        if self._head is None:
            # empty list
            self._head = self._tail = new_node
        else:
            # link nodes together
            self._tail.next = new_node
            new_node.prev = self._tail
            # update tail
            self._tail = new_node
        return new_node

    def push(self, data):
        return self.append(data)

    def push_left(self, data):
        new_node = DoublyNode(data, dll=self, next_=self._head)
        self._head.prev = new_node
        self._head = new_node
        self._len += 1
        return new_node

    def remove(self, data, all_instances: bool = False):
        pointer = self._head
        p = None
        while pointer is not None:
            if pointer.data == data:
                self._len -= 1
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

    def pop(self):
        node = self._tail
        self._tail = node.prev
        node.prev = None
        self._tail.next = None
        self._len -= 1
        return node.data

    def pop_left(self):
        node = self._head
        if self._head == self._tail:
            self._head = None
            self._tail = None
        else:
            self._head = node.next
            node.next = None
            self._head.prev = None
        self._len -= 1
        return node.data

    def __len__(self):
        return self._len

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

