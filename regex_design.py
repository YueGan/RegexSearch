class Node:
    '''
    A node class that would represent all the node classes
    '''
    
    def __init__(self, data, left=None, right=None):
        """ (Node, str, Node, Node) -> NoneType

        Initialize a new BinTreeNode with data, left and right children.
        """

        self.data = data
        self.left = left
        self.right = right

    def __repr__(self):
        """ (Node) -> str

        Return a string representing self.
        """

        return ("Node(" + repr(self.data) + ", " +
                repr(self.left) + ", " + repr(self.right) + ")")
    
    def __eq__(self: 'Node', other: 'Node'):
        """ (Node) -> bool
        
        Compares two nodes.
        """
        
         
        return self.data == other.data
    
