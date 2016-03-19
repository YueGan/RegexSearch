class BinTreeNode:
    """
    A node in a binary tree.
    """

    def __init__(self, data, left=None, right=None):
        """ (BinTreeNode, str, BinTreeNode, BinTreeNode) -> NoneType

        Initialize a new BinTreeNode with data, left and right children.
        """

        self.data = data
        self.left = left
        self.right = right

    def __repr__(self):
        """ (BinTreeNode) -> str

        Return a string representing self.
        """

        return ("BinTreeNode(" + repr(self.data) + ", " +
                repr(self.left) + ", " + repr(self.right) + ")")

    def visit(self):
        """ (BinTreeNode) -> NoneType

        Visit the node self.  In this case we print its data.
        """

        print(self.data)


def preorder(root):
    """ (BinTreeNode) -> NoneType

    Visit the nodes of the tree rooted at root
    using preorder traversal.
    """

    if root != None:
        root.visit()
        preorder(root.left)
        preorder(root.right)


def postorder(root):
    """ (BinTreeNode) -> NoneType

    Visit the nodes of the tree rooted at root
    using postorder traversal.
    """

    if root != None:
        postorder(root.left)
        postorder(root.right)
        root.visit()


def inorder(root):
    """ (BinTreeNode) -> NoneType

    Visit the nodes of the tree rooted at root
    using inorder traversal.
    """

    if root != None:
        inorder(root.left)
        root.visit()
        inorder(root.right)


def bst_search(root, value):
    """ (BinTreeNode, str) -> bool

    Return True iff the BST rooted at root
    contains a node whose data is value.
    """

    curr = root
    while curr != None and curr.data != value:
        if value < curr.data:
            curr = curr.left
        else:
            curr = curr.right

    return (curr != None)


def bst_search_rec(root, value):
    """ (BinTreeNode, str) -> bool

    Return True iff the BST rooted at root
    contains a node whose data is value.
    """

    if root == None:
        return False

    if value < root.data:
        return bst_search_rec(root.left, value)
    elif value > root.data:
        return bst_search_rec(root.right, value)
    else:
        return True


def bst_insert(root, value):
    """ (BinTreeNode, str) -> BinTreeNode

    Insert a (possibly duplicate) node whose data is value
    into the BST rooted at root.
    Return the root of the updated BST.
    """

    new_node = BinTreeNode(value)

    # look for parent of new node
    curr = root
    parent = None
    while curr != None:
        parent = curr
        if value < curr.data:
            curr = curr.left
        else:
            curr = curr.right

    # empty BST, no parent
    if parent == None:
        return new_node

    # make new node appropriate child of parent
    if value < parent.data:
        parent.left = new_node
    else:
        parent.right = new_node
    return root


def bst_insert_rec(root, value):
    """ (BinTreeNode, str) -> BinTreeNode

    Insert a (possibly duplicate) node whose data is value
    into the BST rooted at root.
    Return the root of the updated BST.
    """

    if root == None:
        return BinTreeNode(value)

    if value < root.data:
        root.left = bst_insert_rec(root.left, value)
    else:
        root.right = bst_insert_rec(root.right, value)
    return root


def bst_find(root, value):
    """ (BinTreeNode, str) -> (BinTreeNode, BinTreeNode)

    Return 2 nodes, the first pointing the a node
    in the BST rooted at root whose data is value,
    and the second is its parent.

    For each of these nodes,
    return None if it does not exist.
    """

    # search for node whose data is value
    curr = root
    parent = None
    while curr != None and curr.data != value:
        parent = curr
        if value < curr.data:
            curr = curr.left
        else:
            curr = curr.right

    # if node not found
    if curr == None:
        return (None, None)
    else:
        return (curr, parent)


def bst_find_smallest(root):
    """ (BinTreeNode) -> (BinTreeNode, BinTreeNode)

    Return a node with the smallest value
    in the BST rooted at root, plus its parent.

    REQ: root != None (i.e, the BST is not empty).
    """

    # finding smallest is same as finding left most
    curr = root
    parent = None
    while curr.left != None:
        parent = curr
        curr = curr.left

    return (curr, parent)

"""
Interesting exercises:

1. Write a recursive version of bst_find_smallest().

2. Write a function that finds the node with the second smallest value.
   I.e., the second node visited on an inorder traversal.
"""


def bst_delete(root, value):
    """ (BinTreeNode, str) -> BinTreeNode

    Delete a node whose data is value
    from the BST rooted at root.
    Return the root of the updated BST.

    The BST is unchanged if it does not
    contain a node whose data is value.
    """

    (del_node, del_parent) = bst_find(root, value)

    # return old root if value not found
    if del_node == None:
        return root

    # if node to delete has no left child
    if del_node.left == None:
        # if node to delete is root
        if del_parent == None:
            root = del_node.right
        # elif node to delete is a left child
        elif del_parent.left == del_node:
            del_parent.left = del_node.right
        # else node to delete must be a right child
        else:
            del_parent.right = del_node.right

    # elif node to delete has no right child
    elif del_node.right == None:
        # if node to delete is root
        if del_parent == None:
            root = del_node.left
        # elif node to delete is a left child
        elif del_parent.left == del_node:
            del_parent.left = del_node.left
        # else node to delete must be a right child
        else:
            del_parent.right = del_node.left

    # else node to delete has both children
    else:
        # find node with next bigger value
        (next, next_parent) = bst_find_smallest(del_node.right)

        # copy data from next bigger node to node to delete
        del_node.data = next.data

        # delete next biggest node
        # if next biggest node is right child of node to delete
        if next_parent == None:
            del_node.right = next.right
        else:
            next_parent.left = next.right

    return root

"""
Exercise:
Modify bst_delete() so that, instead of finding the node with
the next bigger value, we find the next smaller one.
"""


if __name__ == "__main__":

    # what does the following tree look like?
    root = BinTreeNode("A",
        BinTreeNode("B",
            BinTreeNode("C", None, None),
            BinTreeNode("D", None, None)),
        BinTreeNode("E",
            BinTreeNode("F", None, None),
            BinTreeNode("G", None, None)))

    # what does this binary search tree (BST) look like?
    bst_root = BinTreeNode("N",
        BinTreeNode("I",
            BinTreeNode("C",
                BinTreeNode("A", None, None),
                BinTreeNode("H", None, None)),
            BinTreeNode("L", None, None)),
        BinTreeNode("O",
            None,
            BinTreeNode("S", None, None)))

"""
Exercise:
It would be helpful to see what our tree look like.
Write a function to do that.
Advice: Consider the directory example from Brian,
 but put a node's right subtree on lines above the node,
 and its left subtree on lines below the node.
 So if we tilt our heads to the left, the tree looks proper.
"""
