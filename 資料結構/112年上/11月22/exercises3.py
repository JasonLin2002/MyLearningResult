class TreeNode:
    def __init__(self, key:str):
        self.key = key
        self.children = []
class BTreeNode:
    def __init__(self, key:str):
        self.key = key
        self.left = None
        self.right = None 
def tree_to_binary_tree(root:TreeNode, right:list=[])->BTreeNode:
    if (not root):
        return None
    else:
        Broot = BTreeNode(root.key)
        if (len(root.children) > 0):
            Broot.left = tree_to_binary_tree(root.children[0], root.children[1:])
        if (len(right) > 0):
            Broot.right = tree_to_binary_tree(right[0], right[1:])
        return Broot
def pre_order_traversal(root:BTreeNode):
    if (not root):
        return
    else:
        print(root.key, end="")
        pre_order_traversal(root.left)
        pre_order_traversal(root.right)
def in_order_traversal(root:BTreeNode):
    if (not root):
        return
    else:
        in_order_traversal(root.left)
        print(root.key, end="")
        in_order_traversal(root.right)
def post_order_traversal(root:BTreeNode):
    if (not root):
        return
    else:
        post_order_traversal(root.left)  
        post_order_traversal(root.right) 
        print(root.key, end="")

if __name__ == "__main__":
    t1 = {}
    for i in range(65, 88):
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
    
    r2 = t1["O"]
    
    r2.children.append(t1["P"])
    
    r2.children[0].children.append(t1["Q"])
    r2.children[0].children.append(t1["R"])
    r2.children[0].children.append(t1["S"])
    
    r3 = t1["T"]
    
    r3.children.append(t1["U"])
    r3.children.append(t1["V"])
    
    r3.children[1].children.append(t1["W"])
    
    br1 = tree_to_binary_tree(r1, [r2, r3])
    
    pre_order_traversal(br1)
    print()
    in_order_traversal(br1)
    print()
    post_order_traversal(br1)