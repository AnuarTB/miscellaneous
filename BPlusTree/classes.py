"""
classes.py
Implements Node, BPlustree and Interface
"""
import re
import sys
import collections

def split_list(arr, divider):
    return arr[:divider], arr[divider:]

"""Finds position of the key in the sorted array arr

Args:
    key: a variable of the same type as elements of array
"""
def find_pos(arr, key):
    pos = 0
    while pos < len(arr) and key >= arr[pos]:
        pos += 1
    return pos

class Node(object):
    """The class implements the B+ tree node structure 
    
    Args:
        parent: a parent of the node. For root it is None.
        children: an array containing children nodes
        keys: an array of keys in the node
        values: the array containing data (applicable to leaves)
        right: a right brother node of the node (applicable to leaves)
        right: a left brother node of the node (applicable to leaves)
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.keys = []
        self.values = []
        self.right = None
        self.left = None
    
    def __str__(self):
        if self.leaf():
            return str(list(zip(self.keys, self.values)))
        else:
            return str(self.keys)

    def leaf(self):
        return not self.children

class BPlusTree(object):
    """The class that implements B+ tree

    Args: 
        order (int): the order of B+ tree, i.e it means that the non-root node 
            can have number of children between order and 2 * order.   
    """
    def __init__(self, order=2):
        self.root = Node()
        self.order = order
    
    """Finds leaf by key

    Args: 
        key: the key by which the B+ tree need to find leaf
    Returns:
        a leaf that can key 
    """
    def find_leaf(self, key):
        cur = self.root
        while not cur.leaf():
            for i, node_key in enumerate(cur.keys):
                if key < node_key:
                    cur = cur.children[i]
                    break
            else:
                cur = cur.children[-1]
        return cur
    
    """Find all data associated with the key

    Args:
        key: the key by which the data will be searched
    Returns:
        Array with data associated with 'key', if there is no such key in tree
        returns []. 
    """
    def find_values(self, key):
        node = self.find_leaf(key)
        if key not in node.keys:
            return []
        else:
            return node.values[node.keys.index(key)]
    """Inserts a (key, value) pair into B+ tree

    If key exists in tree, the value is added in the node to the array of values

    Args: 
        key: a key by which the tree will be queried
        val: the variable containing some data
    """
    def insert(self, key, val):
        node = self.find_leaf(key)
        if key in node.keys:
            node.values[node.keys.index(key)].append(val)
            return
        
        pos = find_pos(node.keys, key)
        
        node.keys.insert(pos, key)
        node.values.insert(pos, [val])

        if len(node.keys) == self.order * 2:
            self.split(node)
    """Splits node if it is full

    Args: 
        node: a node to split
    """
    def split(self, node):
        new_node = Node()
        new_node.right = node
        new_node.left = node.left
        node.left = new_node
        new_node.parent = node.parent

        mid_key = node.keys[self.order]

        new_node.keys, node.keys = split_list(node.keys, self.order)
        new_node.values, node.values = split_list(node.values, self.order)

        if not node.leaf():
            node.keys.pop(0)

        if node is self.root:
            self.root = Node()
            node.parent = self.root
            new_node.parent = self.root
            self.root.children.append(node)
        
        par = node.parent
        pos = find_pos(par.keys, mid_key)

        par.children.insert(pos, new_node)
        par.keys.insert(pos, mid_key)

        if len(par.keys) == self.order * 2:
            self.split(par)
    
    """Delete a (key, value) pair from B+ tree
    
    NOTE: If there are several values with a certain key, only value will be 
    deleted from the tree. Otherwise, the whole node will be deleted. 

    Args:
        key: the key by which the data will be deleted
        val: a data that need to be deleted 
    Returns:
        True if such key exists in tree, otherwise False
    """
    def delete(self, key, val):
        node = self.find_leaf(key)

        if key not in node.keys:
            return False
        
        self.delete_key(node, key, val)
        return True
    
    """Delete a key from a B+ tree
    
    Args:
        node: a node from which the key will be deleted 
        key: key which exists in node
        val: if provided indicates that the key is deleted from leaf
    
    """
    def delete_key(self, node, key, val=None):
        pos = node.keys.index(key)
        if node.leaf():
            node.values[pos].remove(val)
            if not node.values[pos]:
                node.values.pop(pos)
            else:
                return
        else:
            node.children.pop(pos + 1)
        old_key = node.keys.pop(pos)
        if not pos and node.keys: #TODO
            self.replace_key(node.parent, old_key, node.keys[0])
        if node is self.root and not node.keys:
            self.root = self.root.children[0]
            self.root.parent = None
            return
        if len(node.keys) >= self.order - 1:
            return True
        l_node = node.left
        r_node = node.right
        if l_node and len(l_node.keys) >= self.order:
            node.keys.insert(0, l_node.keys[-1])
            l_node.keys.pop()
            if l_node.values:
                node.values.insert(0, l_node.values[-1])
                l_node.values.pop()
            if l_node.children:
                node.children.insert(0, l_node.children[-1])        
                l_node.children.pop()
            self.replace_key(node.parent, node.keys[1], node.keys[0])
        
        elif r_node and len(r_node.keys) >= self.order:
            node.keys.append(r_node.keys[0])
            r_node.keys.pop(0)
            if r_node.values:
                node.values.append(r_node.values[0])
                r_node.values.pop(0)
            if r_node.children:
                node.children.append(r_node.children[0])        
                r_node.children.pop(0)
            self.replace_key(node.parent, node.keys[-1], r_node.keys[0])
        
        else:
            if l_node:
                l_node.keys += node.keys
                l_node.values += node.values
                l_node.children += node.children

                l_node.right = node.right
                if l_node.right:
                    l_node.right.left = l_node

                self.delete_key(l_node.parent, old_key)
            else:
                node.keys += r_node.keys
                node.values += r_node.values
                node.children += r_node.children

                node.right = r_node.right
                if node.right:
                    node.right.left = node

                self.delete_key(node.parent, r_node.keys[0])
    
    """Replaces old key with new key starting from node
    all the way up to the root.

    Args: 
        node: a node to start replacing from
        old_key: a value of key to be replaced
        new_key: a value of key which will replace old key
    """    
    def replace_key(self, node, old_key, new_key):
        if not node:
            return
        if old_key in node.keys:
            node.keys[node.keys.index(old_key)] = new_key
        self.replace_key(node.parent, old_key, new_key)
    
    def print_tree(self):
        self.print(self.root)
    
    """Prints node information in the format

    The tree traversal is postorder

    Args: 
        node: a node to be printed

    Example:
        For leaf node:

        ------
        Keys: [1, 5, 8]
        Values: [[3], [2], [1, 4]]
        # of children: 0
        ------
        
        For internal node:
        
        ------
        Keys: [1, 5, 8]
        Values: []
        # of children: 4 
        ------

    """
    def print(self, node):
        print("------")
        print("Keys: {}".format(node.keys))
        print("Values: {}".format(node.values))
        print("# of children: {}".format(len(node.children)))
        print("------")
        for child in node.children:
            self.print(child)

class Database(object):
    def __init__(self, tree, table_file):
        self.tree = tree
        self.table_file = table_file
        self.table = []
        self.f_key = 0
        self.s_key = 0
        self.attrs = []
        if self.table_file:
            with open(self.table_file, "r") as f:
                self.attrs = f.readline().strip().split(',')
                print("Choose two attributes which will serve as key for the database.")
                for i, attr in enumerate(self.attrs):
                    print("{}: {}".format(i + 1, attr))
                self.f_key = int(input("Please enter the attribute number for the first key: ")) - 1
                self.s_key = int(input("Please enter the attribute number for the second key: ")) - 1
                for line in f:
                    self.table.append(line.strip().split(','))
    
    def key(self, id):
        return (
            self.table[id][self.f_key],
            self.table[id][self.s_key])

    def val(self, id):
        return id + 1

    def load(self):
        print("=========== LOAD ============")
        s_id = int(input("LOAD_START_TID: ")) - 1
        f_id = int(input("LOAD_END_TID: ")) - 1
        print("LOADING...")
        self.tree = BPlusTree()
        for i in range(s_id, f_id + 1):
            self.tree.insert(self.key(i), self.val(i))
        print("B+ Tree is built")

    def print(self):
        print("========== PRINT ============")
        q = collections.deque()
        q.append((self.tree.root, 1))
        out_arr = []
        while q:
            node, lvl = q.popleft()
            if lvl > len(out_arr):
                out_arr.append([])
            if node.leaf():
                out_arr[lvl - 1].append(list(zip(node.keys, node.values)))
            else:
                out_arr[lvl - 1].append(node.keys)
            for child in node.children:
                q.append((child, lvl + 1))
        for lvl, nodes in enumerate(out_arr):
            print("Level {}: {}".format(lvl + 1, nodes))

    def insert(self):
        print("========== INSERT ===========")
        t_id = int(input("TUPLE ID: ")) - 1
        self.tree.insert(self.key(t_id), self.val(t_id))
        print("Tuple #{} is inserted".format(t_id + 1))
    
    def delete(self):
        print("========== DELETE ===========")
        t_id = int(input("TUPLE ID: ")) - 1
        self.tree.delete(self.key(t_id), self.val(t_id))
        print("Tuple #{} is deleted".format(t_id + 1))

    def search(self):
        print("========== SEARCH ===========")
        print((
            "Please enter the key without extra whitespaces\n"
            "in the format: \n"
            "(key1,key2)\n"))
        key_str = input("SEARCH KEY: ")
        key_regex = re.compile(r"\((.+?),(.+?)\)", re.DOTALL)
        key = re.match(key_regex, key_str)
        key = (key.group(1), key.group(2))
        vals = self.tree.find_values(key)
        print("Found tuple IDs: {}".format(vals))
        print("Attributes: < {} >".format(", ".join(self.attrs)))
        for val in vals:
            print("Tuple #{}: < {} >".format(val, ", ".join(self.table[val - 1])))

    def range_search(self):
        print("======== RANGE SEARCH =======")
        print((
            "Please enter the range of keys without extra whitespaces\n"
            "in the format: \n"
            "[(key1,key2),(key3,key4)]\n"))
        range_str = input("SEARCH RANGE: ")
        range_regex = re.compile(r"\[\((.+?),(.+?)\),\((.+?),(.+?)\)\]", re.DOTALL)
        tmp = re.match(range_regex, range_str)
        start_key = (tmp.group(1), tmp.group(2))
        finish_key = (tmp.group(3), tmp.group(4))
        node = self.tree.find_leaf(start_key)
        res = []
        vals = []
        boo = True
        while node and boo:
            for i, key in enumerate(node.keys):
                if key > finish_key:
                    boo = False
                    break
                if start_key <= key <= finish_key:
                    res.append((key, node.values[i]))
                    vals += node.values[i]
            node = node.right
        print("Found pairs: {}".format(res))
        print("Attributes: < {} >".format(", ".join(self.attrs)))
        for val in vals:
            print("Tuple #{}: < {} >".format(val, ", ".join(self.table[val - 1])))
        
    def exit(self):
        sys.exit(0)