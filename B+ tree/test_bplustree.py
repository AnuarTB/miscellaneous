"""
test_bplustree.py
Module for testing the implementation of database
"""
import unittest

from classes import BPlusTree, split_list, find_pos

class BPlusTreeMethods(unittest.TestCase):

    def test_find_pos(self):
        self.assertEqual(find_pos([], 1), 0)
        self.assertEqual(find_pos([3, 5, 7, 9], 6), 2)
        self.assertEqual(find_pos([5, 6, 7, 8], 2), 0)
        self.assertEqual(find_pos([4, 10, 12], 13), 3)

    def test_split_list(self):
        self.assertEqual(split_list([1, 2, 3, 4, 5], 1), ([1], [2, 3, 4, 5]))
        self.assertEqual(split_list([1, 2, 3], 0), ([], [1, 2, 3]))
        self.assertEqual(split_list([1, 2, 3], 3), ([1, 2, 3], []))
        self.assertEqual(split_list([], 4), ([], []))

    def test_insert(self):
        tree = BPlusTree()
        tree.insert((1, 1), "A")
        tree.insert((1, 1), "C")
        tree.insert((1, 1), "B")
        self.assertEqual(tree.root.values[0], ["A", "C", "B"])
        tree.insert((1, 2), "D")
        self.assertEqual(tree.root.keys, [(1, 1), (1, 2)])
        tree.insert((1, 0), "E")
        self.assertEqual(tree.root.keys, [(1, 0), (1, 1), (1, 2)])
        tree.insert((1, 3), "F")
        self.assertEqual(tree.root.keys, [(1, 2)])

    def test_find(self):
        tree = BPlusTree()
        tree.insert((1, 1), "A")
        tree.insert((1, 1), "C")
        tree.insert((1, 1), "B")
        tree.insert((1, 2), "D")
        tree.insert((1, 0), "E")
        tree.insert((1, 3), "F")
        self.assertEqual(tree.find_values((1, 1)), ['A', 'C', 'B'])
        self.assertEqual(tree.find_values((0, 1)), [])
        self.assertEqual(tree.find_values((100, 0)), [])
    
    def test_delete(self):
        tree = BPlusTree()
        tree.insert((1, 1), "A")
        tree.insert((1, 1), "C")
        tree.insert((1, 1), "B")
        tree.insert((1, 2), "D")
        tree.insert((1, 0), "E")
        tree.insert((1, 3), "F")
        self.assertEqual(tree.find_values((1, 1)), ['A', 'C', 'B'])
        self.assertEqual(tree.find_values((0, 1)), [])
        tree.delete((1, 1), "C")
        self.assertEqual(tree.find_values((1, 1)), ['A', 'B'])
        tree.delete((1, 1), "A")
        self.assertEqual(tree.find_values((1, 1)), ['B'])
        tree.delete((1, 1), "B")
        self.assertEqual(tree.find_values((1, 1)), [])
        tree.delete((1, 0), "E")
        self.assertEqual(len(tree.root.children), 2)
        tree.delete((1, 3), "F")
        self.assertEqual(len(tree.root.children), 0)

if __name__ == "__main__":
    unittest.main()
