class TreeNode:
    def __init__(self, key:int):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None



def returnTree(arr:list, index)->TreeNode:
    if (index >= len(arr) or arr[index]==None):
        return None
    else:
        root = TreeNode(arr[index])
        root.left = returnTree(arr, index*2+1)
        if (root.left):
            root.left.parent = root
        root.right = returnTree(arr, index*2+2)
        if (root.right):
            root.right.parent = root
        return root
    
def covertArrayToTree(arr:list)->TreeNode:
    if (len(arr) != 0):
        return returnTree(arr, 0)
    else:
        return None

def inroder_traversal(root:TreeNode):
    if (not root):
        return
    else:
        inroder_traversal(root.left)
        print("data: ", root.key)
        if (root.parent):
            print("parent: ", root.parent.key)
        else:
            print("parent: ", None)
        if (root.left):
            print("left: ", root.left.key)
        else:
            print("left: ", None)
        if (root.right):
            print("right: ", root.right.key)
        else:
            print("right: ", None)
        print("---"*10)
        inroder_traversal(root.right)

if __name__ == "__main__":
    l1 = [12, 13, 14, 6, 7, 16, None, None, None, None, None, 11, 13]

    root = covertArrayToTree(l1)
    
    inroder_traversal(root)