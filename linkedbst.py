"""
File: linkedbst.py
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
import random
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            variable_s = ""
            if node != None:
                variable_s += recurse(node.right, level + 1)
                variable_s += "| " * level
                variable_s += str(node.data) + "\n"
                variable_s += recurse(node.left, level + 1)
            return variable_s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        current = self._root
        while current is not None:
            if current.data == item:
                break
            elif current.data < item:
                current = current.right
            else:
                current = current.left
        return current

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        if self._root is None:
            self._root = BSTNode(item)
        else:
            current = self._root
            while True:
                if item > current.data:
                    if current.right is not None:
                        current = current.right
                    else:
                        current.right = BSTNode(item)
                        break
                else:
                    if current.left is not None:
                        current = current.left
                    else:
                        current.left = BSTNode(item)
                        break
        self._size += 1

    def remove(self, item):
        """
        Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self.
        """
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = newItem
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top):
            """
            Helper function
            :param top:
            :return:
            """
            if top.left is None and top.right is None:
                return 0
            else:
                return 1 + max(height1(child)
                               for child in [top.left, top.right]
                               if child is not None)

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        """
        return self.height() < 2 * log(len(self) + 1, 2) - 1

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        """

        def tree_to_list(edge):
            if edge.left is not None:
                tree_to_list(edge.left)
            edges_list.append(edge.data)
            if edge.right is not None:
                tree_to_list(edge.right)

        edges_list = []
        tree_to_list(self._root)
        range_list = []
        for elem in edges_list:
            if low <= elem <= high:
                range_list.append(elem)
        return range_list

    def rebalance(self):
        """
        Rebalances the tree.
        """

        def inorder(edge):
            previous = LinkedStack()
            previous.push(edge)
            edge = edge.left
            while len(previous) != 0 or edge is not None:
                if edge is not None:
                    previous.push(edge)
                    edge = edge.left
                else:
                    edge = previous.pop()
                    edges_list.append(edge.data)
                    edge = edge.right

        def create_balance_tree(tree_list):
            if len(tree_list) != 0:
                self.add(tree_list[len(tree_list) // 2])
                create_balance_tree(tree_list[:len(tree_list) // 2])
                create_balance_tree(tree_list[(len(tree_list) // 2 + 1):])

        edges_list = []
        inorder(self._root)
        self.clear()
        create_balance_tree(edges_list)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        """
        current = self._root
        smallest = None
        while current is not None:
            if current.data > item:
                if smallest is not None:
                    if smallest > current.data:
                        smallest = current.data
                else:
                    smallest = current.data
                current = current.left
            else:
                current = current.right
        return smallest

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        """
        current = self._root
        biggest = None
        while current is not None:
            if current.data < item:
                if biggest is not None:
                    if biggest < current.data:
                        biggest = current.data
                else:
                    biggest = current.data
                current = current.right
            else:
                current = current.left
        return biggest

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        """
        with open(path, "r") as file:
            content = file.read()
        content = content.split("\n")
        words = random.sample(content, 10000)
        start = time.time()
        for search_word in words:
            for element in content:
                if search_word == element:
                    break
        end = time.time()
        list_time = end - start
        print(f"Searching in list: {list_time}")
        sorted_tree = LinkedBST()
        for element in content:
            sorted_tree.add(element)
        start = time.time()
        for search_word in words:
            sorted_tree.find(search_word)
        end = time.time()
        sorted_tree_time = end - start
        print(f"Searching in sorted tree: {sorted_tree_time}")
        random.shuffle(content)
        random_tree = LinkedBST()
        for element in content:
            random_tree.add(element)
        start = time.time()
        for search_word in words:
            random_tree.find(search_word)
        end = time.time()
        tree_time = end - start
        print(f"Searching in random tree: {tree_time}")
        random_tree.rebalance()
        start = time.time()
        for search_word in words:
            random_tree.find(search_word)
        end = time.time()
        balanced_tree_time = end - start
        print(f"Searching in balanced tree: {balanced_tree_time}")
