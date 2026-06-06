# id1: 325762771
# name1: Laor Gilboa
# username1: laorgilboa
# id2: 214441610
# name2: Ophir Peleg
# username2: ophirpeleg


"""A class representing a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0 if key is not None else -1

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.key is not None


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    @type is_avl: boolean
    @param is_avl: If True then tree is AVL, otherwise it is just a "regular" binary search tree, without rotations.
    """

    def __init__(self, is_avl):
        self.virtual_node = AVLNode(None, None)
        self.root = self.virtual_node
        self.is_avl = is_avl
        self.size = 0

    
    """updates the height of a given node
    
    @type node: AVLNode
    @param node: the node to update its height
    """
    def update_height(self, node):
        if node.is_real_node():
            node.height = 1 + max(node.left.height, node.right.height)

    """returns the balance factor of a given node
    
    @type node: AVLNode
    @param node: the node to calculate its balance factor
    @rtype: int
    @returns: the balance factor (left.height - right.height), 0 if the node is virtual
    """
    def get_balance_factor(self, node):
        if not node.is_real_node():
            return 0
        return node.left.height - node.right.height


    """performs a left rotation
    
    @type x: AVLNode
    @param x: the node to perform the rotation on
    """
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        
        # Update the parent of the moved sub-tree, only if it's a real node
        if y.left.is_real_node():
            y.left.parent = x
            
        y.parent = x.parent
        
        # Update the original parent's pointer (or update the root if x was the root)
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
            
        y.left = x
        x.parent = y
        
        # Update heights: first the child (x), then the new parent (y)
        self.update_height(x)
        self.update_height(y)

    """performs a right rotation
    
    @type y: AVLNode
    @param y: the node to perform the rotation on
    """
    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        
        # Update the parent of the moved sub-tree, only if it's a real node
        if x.right.is_real_node():
            x.right.parent = y
            
        x.parent = y.parent
        
        # Update the original parent's pointer (or update the root if y was the root)
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
            
        x.right = y
        y.parent = x
        
        # Update heights: first the child (y), then the new parent (x)
        self.update_height(y)
        self.update_height(x)


    """restores the AVL tree property of a given node
    
    @type node: AVLNode
    @param node: the node to balance
    @rtype: int
    @returns: the number of rotations performed (0, 1, or 2)
    """
    def balance(self, node):
        # Check if the tree is a regular BST or if the node is virtual
        if not self.is_avl or not node.is_real_node():
            return 0
            
        balance_factor = self.get_balance_factor(node)
        
        # Left Heavy (exact violation of 2)
        if balance_factor == 2:
            # Left-Right (LR) case
            if self.get_balance_factor(node.left) < 0:
                self.left_rotate(node.left)
                self.right_rotate(node)
                return 2
            # Left-Left (LL) case
            else:
                self.right_rotate(node)
                return 1
                
        # Right Heavy (exact violation of -2)
        elif balance_factor == -2:
            # Right-Left (RL) case
            if self.get_balance_factor(node.right) > 0:
                self.right_rotate(node.right)
                self.left_rotate(node)
                return 2
            # Right-Right (RR) case
            else:
                self.left_rotate(node)
                return 1
                
        # The tree is balanced (BF is 1, 0, or -1), no rotations needed
        return 0

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x, search_time) where x is the node corresponding to key (or None if not found)
    and search_time is the search time, as defined and explained in the assignment.
    """

    def search(self, key):
        return None, -1

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int,int)
    @returns: a 4-tuple (x, search_time, rotations, height_changes), where x is the new node
    and the other 3 return values are as defined and explained in the assignment.
    """

    def insert(self, key, val):
        return None, -1, -1, -1

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    def delete(self, node):
        return

    """returns a list representing dictionary 

    @rtype: list
    @returns: a list of (key, value) tuples sorted by key, representing the data structure
    """

    def avl_to_list(self):
        return None

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return -1

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root

    """returns the height of the tree

        @rtype: int
        @returns: the height of the tree 
        """

    def get_height(self):
        return -1
