class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def addNode(self, data):
        self.root = self._addNode(self.root, data)

    def _addNode(self, root, data):
        if root is None:
            return TreeNode(data)
        if data < root.data:
            root.left = self._addNode(root.left, data)
        elif data > root.data:
            root.right = self._addNode(root.right, data)
        return root

    def in_order(self):
        result = []
        self._in_order(self.root, result)
        print("In-order:", result)

    def _in_order(self, root, result):
        if root:
            self._in_order(root.left, result)
            result.append(root.data)
            self._in_order(root.right, result)

    def pre_order(self):
        result = []
        self._pre_order(self.root, result)
        print("Pre-order:", result)

    def _pre_order(self, root, result):
        if root:
            result.append(root.data)
            self._pre_order(root.left, result)
            self._pre_order(root.right, result)

    def post_order(self):
        result = []
        self._post_order(self.root, result)
        print("Post-order:", result)

    def _post_order(self, root, result):
        if root:
            self._post_order(root.left, result)
            self._post_order(root.right, result)
            result.append(root.data)

    def findLevel(self, data):
        level = self._findLevel(self.root, data, 0)
        if level is not None:
            print(f"Level of {data}: {level}")
        else:
            print(f"{data} not found in the tree.")

    def _findLevel(self, root, data, level):
        if root is None:
            return None
        if data == root.data:
            return level
        elif data < root.data:
            return self._findLevel(root.left, data, level + 1)
        else:
            return self._findLevel(root.right, data, level + 1)

bst = BinarySearchTree()
data_list = [11, 6, 13, 5, 9, 31, 3, 7, 29, 1, 4]
for data in data_list:
    bst.addNode(data)

bst.in_order()
bst.pre_order()
bst.post_order()

# 尋找特定數值的Level
bst.findLevel(9)
bst.findLevel(29)
