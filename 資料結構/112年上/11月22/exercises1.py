class TreeNode:
    def __init__(self, key:str):
        self.key = key
        self.children = []
def pre_order_traversal(root:TreeNode):
    if (not root):
        return
    else:
        print(root.key, end="")
        for child in root.children:
            pre_order_traversal(child)
def in_order_traversal(root:TreeNode):
    if (not root):
        return
    else:
        for child in root.children[:1]:
            in_order_traversal(child)
        print(root.key, end="")
        for child in root.children[1:]:
            in_order_traversal(child)
def post_order_traversal(root:TreeNode):
    if (not root):
        return
    else:
        for child in root.children:
            post_order_traversal(child)
        print(root.key, end="")

if __name__ == "__main__":
    t1 = {}
    for i in range(65, 79):
        t1[chr(i)] = TreeNode(chr(i))

    r1 = t1["A"]
    
    r1.children.append(t1["B"])
    r1.children.append(t1["C"])
    r1.children.append(t1["D"])
    
    r1.children[0].children.append(t1["E"])
    r1.children[1].children.append(t1["F"])
    r1.children[1].children.append(t1["G"])
    r1.children[1].children.append(t1["H"])
    r1.children[2].children.append(t1["I"])
    
    r1.children[0].children[0].children.append(t1["J"])
    r1.children[0].children[0].children.append(t1["K"])
    r1.children[1].children[0].children.append(t1["L"])
    r1.children[1].children[0].children.append(t1["M"])
    r1.children[1].children[2].children.append(t1["N"])
    
    pre_order_traversal(r1)
    print()
    in_order_traversal(r1)
    print()
    post_order_traversal(r1)