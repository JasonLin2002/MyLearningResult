class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def build_tree(preorder, inorder):
    if not preorder or not inorder:
        return None

    root_value = preorder[0]
    root = TreeNode(root_value)

    root_index = inorder.index(root_value)

    root.left = build_tree(preorder[1:1 + root_index], inorder[:root_index])
    root.right = build_tree(preorder[1 + root_index:], inorder[root_index + 1:])

    return root

def post_order(root):
    if root:
        post_order(root.left)
        post_order(root.right)
        print(root.data, end=' ')

preorder = [12, 6, 10, 7, 8, 11, 20, 15, 24, 21, 22]
inorder = [6, 7, 8, 10, 11, 12, 15, 20, 21, 22, 24]

root = build_tree(preorder, inorder)

print("Post-order:", end=' ')
post_order(root)