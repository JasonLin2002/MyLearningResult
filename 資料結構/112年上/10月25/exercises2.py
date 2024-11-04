class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularList:
    def __init__(self):
        self.head = None

    def traverse(self):
        if not self.head:
            return

        current = self.head
        while True:
            print(current.data)
            current = current.next
            if current == self.head:
                break

    def insertion(self, index, data):
        new_node = Node(data)
        if not self.head:
            new_node.next = new_node
            self.head = new_node
        elif index == 0:
            new_node.next = self.head.next
            self.head.next = new_node
        else:
            current = self.head
            for _ in range(index-1):
                current = current.next
                if current == self.head:
                    raise IndexError("Index out of range")
            new_node.next = current.next
            current.next = new_node

    def search_by_index(self, index):
        if not self.head:
            raise IndexError("List is empty")
        current = self.head
        for _ in range(index):
            current = current.next
            if current == self.head:
                raise IndexError("Index out of range")
        return current.data

    def search_by_value(self, value):
        if not self.head:
            return None
        current = self.head
        while True:
            if current.data == value:
                return current
            current = current.next
            if current == self.head:
                return None

    def deletion(self, index):
        if not self.head:
            raise IndexError("List is empty")
        if index == 0:
            if self.head.next == self.head:
                self.head = None
            else:
                temp = self.head
                while temp.next != self.head:
                    temp = temp.next
                temp.next = self.head.next
                self.head = temp.next
        else:
            current = self.head
            for _ in range(index-1):
                current = current.next
                if current == self.head:
                    raise IndexError("Index out of range")
            current.next = current.next.next

    def update(self, index, data):
        if not self.head:
            raise IndexError("List is empty")
        current = self.head
        for _ in range(index):
            current = current.next
            if current == self.head:
                raise IndexError("Index out of range")
        current.data = data
