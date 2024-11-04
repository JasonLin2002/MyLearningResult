class Node:
    def __init__(self, data:int):
        self.data = data
        self.prev = None
        self.next = None
    
    
    
class Doubly_Linked_List:
    def __init__(self):
        self.head = None
    
    
    
    def append(self, data:int):
        if (not self.head):
            self.head = Node(data)
        else:
            temp = self.head
            while (temp.next):
                temp = temp.next
            temp.next = Node(data)
            temp.next.prev = temp

    def traverse(self):
        temp = self.head
        while (temp):
            print(temp.data, "<-> ", end="")
            temp = temp.next
        print("NULL")
    
    
    
    def search(self, target:int)->int:
        temp = self.head
        index = 0
        while (temp):
            if (temp.data == target):
                return index
            temp = temp.next
            index += 1
        return -1

    def insert(self, index:int, data:int):
        if (index >= 0):
            temp = self.head
            self.head = Node(0)
            self.head.next = temp
            if (temp):
                temp.prev = self.head
            temp = self.head
            temp_next = temp.next
            curr_index = 0
            while (temp_next):
                if (curr_index == index):
                    temp.next = Node(data)
                    temp.next.prev = temp
                    temp.next.next = temp_next
                    temp_next.prev = temp.next
                    del_node = self.head
                    self.head = self.head.next
                    self.head.prev = None
                    del del_node
                    return
                temp = temp.next
                temp_next = temp_next.next
                curr_index += 1
            temp.next = Node(data)
            temp.next.prev = temp
            del_node = self.head
            self.head = self.head.next
            self.head.prev = None
            del del_node
            return 
        else:
            print("Error index")

    def delete(self, index:int):
        if (self.head):
            if (index >= 0):
                temp = self.head
                self.head = Node(0)
                self.head.next = temp
                temp.prev = self.head
                temp = self.head
                curr_index = -1
                while (temp.next):
                    if (curr_index+1 == index):
                        del_node = temp.next
                        temp.next = temp.next.next
                        if (temp.next):
                            temp.next.prev = temp
                        del del_node
                        del_node = self.head
                        self.head = self.head.next
                        if (self.head):
                            self.head.prev = None
                        del del_node
                        return
                    curr_index += 1
                    temp = temp.next
                print("The index out of the range")
                del_node = self.head
                self.head = self.head.next
                self.head.prev = None
                del del_node
            else:
                print("The list is empty")


    def update(self, index:int, data:int):
        if (index >= 0):
            temp = self.head
            curr_index = 0
            while (temp):
                if (curr_index == index):
                    temp.data = data
                    return
                curr_index += 1
                temp = temp.next
            print("The index out of the range")
        else:
            print("Error index")
