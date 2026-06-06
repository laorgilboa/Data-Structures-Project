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
        self.tree_size = 0

    
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
    

    """returns the height of the tree

    @rtype: int
    @returns: the height of the tree 
    """
    def get_height(self):
        # An empty tree is a tree whose root is the virtual node
        if not self.root.is_real_node():
            return -1
            
        # In an AVL tree, we return the height field directly in O(1)
        if self.is_avl:
            return self.root.height
        # In a regular BST, we calculate the height recursively in O(n)
        else:
            return self._calculate_height_recursive(self.root)

    """helper function to calculate the height of a BST recursively in O(n)
    
    @type node: AVLNode
    @param node: the root of the sub-tree
    @rtype: int
    @returns: the height of the sub-tree
    """
    def _calculate_height_recursive(self, node):
        if not node.is_real_node():
            return -1
        return 1 + max(self._calculate_height_recursive(node.left), 
                       self._calculate_height_recursive(node.right))

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x, search_time) where x is the node corresponding to key (or None if not found)
    and search_time is the search time, as defined and explained in the assignment.
    """

    def search(self, key):
        current = self.root
        nodes_visited = 0
        
        while current.is_real_node():
            nodes_visited += 1
            if key == current.key:
                # Successful search
                return current, nodes_visited
            elif key < current.key:
                current = current.left
            else:
                current = current.right
                
        # Failed search (also covers the empty tree case perfectly)
        return None, nodes_visited + 1

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
        # Phase 1: Search for the insertion point
        current = self.root
        parent = None
        nodes_visited = 0
        
        while current.is_real_node():
            nodes_visited += 1
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right
                
        search_time = nodes_visited + 1
        
        # Create the new real node and attach the shared virtual node as its children
        new_node = AVLNode(key, val)
        new_node.left = self.virtual_node
        new_node.right = self.virtual_node
        new_node.parent = parent
        
        # Connect the new node to the tree structure
        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.tree_size += 1
            
        rotations = 0
        height_changes = 0
        
        # Phase 2: Update heights and balance the tree (AVL only)
        if self.is_avl:
            curr_update = parent

            while not curr_update is None and curr_update.is_real_node():
                old_height = curr_update.height
                self.update_height(curr_update)
                new_height = curr_update.height
                
                bf = abs(self.get_balance_factor(curr_update))
                
                # Case 3.2: Balance Factor is OK and height hasn't changed -> terminate
                if bf < 2 and old_height == new_height:
                    break
                    
                # Case 3.3: Balance Factor is OK but height changed -> count it and go up
                elif bf < 2 and old_height != new_height:
                    height_changes += 1
                    curr_update = curr_update.parent
                    
                # Case 3.4: Balance Factor is violated -> perform rotations
                elif bf == 2:
                    rots = self.balance(curr_update)
                    rotations += rots
                    # Move up to the parent (which is now the promoted node after rotation)
                    curr_update = curr_update.parent
                    
        return new_node, search_time, rotations, height_changes

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    def delete(self, node):
        # Phase 1: Delete the correct node
        if not node.is_real_node():
            return

        self.tree_size -= 1
        physically_deleted_parent = None

        # CASES 1 & 2: Node has 0 or 1 real children
        if self.is_leaf(node) or self.has_one_child(node):
            physically_deleted_parent = node.parent
            self.bypass_node(node)
            
        # CASE 3: Node has 2 real children -> transfer the successor and delete its original node
        else:
            successor = self.get_successor(node)
            physically_deleted_parent = successor.parent
            
            node.key = successor.key
            node.value = successor.value
            
            # Physically delete the successor instead
            self.bypass_node(successor)
            
        # If the tree is now empty, no balancing is needed
        if self.tree_size == 0 or not self.is_avl:
            return

        # Phase 2: Update heights and balance the tree (AVL only)
        curr_update = physically_deleted_parent
        
        while curr_update is not None and curr_update.is_real_node():
            old_height = curr_update.height
            self.update_height(curr_update)
            new_height = curr_update.height
            
            bf = abs(self.get_balance_factor(curr_update))
            
            # 3.2: Balance Factor is OK and height hasn't changed -> terminate
            if bf < 2 and old_height == new_height:
                break
                
            # 3.3: Balance Factor is OK but height changed -> go up
            elif bf < 2 and old_height != new_height:
                curr_update = curr_update.parent
                
            # 3.4: Balance Factor is violated -> perform rotations
            elif bf == 2:
                self.balance(curr_update)
                curr_update = curr_update.parent

    # Helper methods for delete()

    """physically bypasses a node that has at most one real child
    
    @type node: AVLNode
    @param node: the node to physically remove from the tree structure
    """
    def bypass_node(self, node):
        # Identify the single child (if it's a leaf, this safely grabs a virtual node)
        child = node.left if node.left.is_real_node() else node.right
        
        # Connect the parent to the child
        if node.parent is None:
            self.root = child
        elif node == node.parent.left:
            node.parent.left = child
        else:
            node.parent.right = child
            
        # Update the child's parent pointer (ONLY if it's a real node)
        if child.is_real_node():
            child.parent = node.parent
    
    """finds the node with the minimum key in a given subtree
    
    @type node: AVLNode
    @param node: the root of the subtree to search
    @rtype: AVLNode
    @returns: the node with the minimum key in the subtree
    """
    def get_minimum(self, node):
        if not node.is_real_node():
            return node
            
        current = node
        while current.left.is_real_node():
            current = current.left
            
        return current

    """finds the in-order successor of a given node
    
    @type node: AVLNode
    @param node: the node to find the successor for
    @rtype: AVLNode
    @returns: the successor node, or None if no successor exists
    """
    def get_successor(self, node):
        if not node.is_real_node():
            return None
            
        if node.right.is_real_node():
            return self.get_minimum(node.right)
            
        current = node
        parent = node.parent
        
        while parent is not None and current == parent.right:
            current = parent
            parent = parent.parent
            
        return parent

    """checks if a given node is a leaf
    
    @type node: AVLNode
    @param node: the node to check
    @rtype: bool
    @returns: True if the node is a leaf (both children are virtual), False otherwise
    """
    def is_leaf(self, node):
        if not node.is_real_node():
            return False
            
        return not node.left.is_real_node() and not node.right.is_real_node()

    """checks if a given node has exactly one real child
    
    @type node: AVLNode
    @param node: the node to check
    @rtype: bool
    @returns: True if the node has exactly one real child, False otherwise
    """
    def has_one_child(self, node):
        if not node.is_real_node():
            return False
            
        left_is_real = node.left.is_real_node()
        right_is_real = node.right.is_real_node()
        return left_is_real != right_is_real

    """returns a list representing dictionary 

    @rtype: list
    @returns: a list of (key, value) tuples sorted by key, representing the data structure
    """

    def avl_to_list(self):
        res = []
        return self.in_order_traverse(self.root, res)


    """helper method for in-order traversal
    
    @type node: AVLNode
    @param node: the root of the current subtree
    @type result: list
    @param result: the list accumulating the sorted tuples
    """

    def in_order_traverse(self, node, res):
        if node.is_real_node():
            self.in_order_traverse(node.left, res)           
            res.append((node.key, node.value))                  
            self.in_order_traverse(node.right, res)             
        return res

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self.tree_size

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root