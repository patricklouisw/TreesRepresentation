"""Assignment 2: Trees for Treemap

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations
import os
import math
from random import randint
from typing import List, Tuple, Optional, Union


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._expanded = False
        self._parent_tree = None
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        # You will change this in Task 5
        if self._name is None:
            self.data_size = 0

            self._subtrees = []

        else:
            if len(self._subtrees) > 0:
                self.data_size = 0

                for subtree in self._subtrees:
                    self.data_size += subtree.data_size
                    subtree._parent_tree = self
            else:

                self.data_size = data_size

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # TODO: (Task 2) Complete the body of this method.
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect
        if self.data_size == 0:
            self.rect = rect
        elif self._subtrees == []:
            self.rect = rect
        else:
            self.rect = rect
            sum1 = self.data_size
            curr_width = rect[0]
            curr_height = rect[1]
            subtrees = self._subtrees
            if rect[2] > rect[3]:
                for i in range(len(self._subtrees) - 1):
                    sub_width = math.floor(subtrees[i].data_size / sum1 *
                                           rect[2])
                    subtrees[i].update_rectangles((curr_width, rect[1],
                                                   sub_width,
                                                   rect[3]))
                    curr_width += sub_width
                last_subtree = subtrees[len(subtrees) - 1]
                last_subtree.update_rectangles((curr_width, rect[1],
                                                rect[2] + rect[0] - curr_width,
                                                rect[3]))
            else:
                for i in range(len(self._subtrees) - 1):
                    sub_height = math.floor(subtrees[i].data_size / sum1 *
                                            rect[3])
                    subtrees[i].update_rectangles((rect[0], curr_height,
                                                   rect[2],
                                                   sub_height))
                    curr_height += sub_height
                last_subtree = subtrees[len(subtrees) - 1]
                last_subtree.update_rectangles((rect[0], curr_height,
                                                rect[2],
                                                rect[3] + rect[1] - curr_height)
                                               )

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self.is_empty():
            return []
        elif self._subtrees == []:
            return [(self.rect, self._colour)]
        else:
            result = []
            if self._expanded is True:
                for subtree in self._subtrees:
                    result.extend(subtree.get_rectangles())
            else:
                result = [(self.rect, self._colour)]
            return result

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.
        """
        if self.is_empty():
            return None
        elif self._subtrees == [] or self._expanded is False:
            if self._helper_leaf_in(pos):
                return self
            else:
                return None
        else:
            result = self._helper_get_possible_list(pos)
            if result == []:
                return None
            elif len(result) == 1:
                return result[0]
            else:
                if isinstance(_helper_get_most_closet(result, pos), bool):
                    return _helper_get_secondary_closet(result, pos)
                else:
                    return _helper_get_most_closet(result, pos)

    def _helper_leaf_in(self, pos: Tuple[int, int]) -> bool:
        if self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2] and \
                self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]:
            return True
        else:
            return False

    def _helper_get_possible_list(self, pos: Tuple[int, int]) -> list:
        result = []
        for subtree in self._subtrees:
            possible = subtree.get_tree_at_position(pos)
            if possible is not None:
                result.append(possible)
        return result

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if self.is_empty():
            self.data_size = 0
            return 0
        elif self._subtrees == []:
            return self.data_size
        else:
            self.data_size = 0
            for subtree in self._subtrees:
                subtree.update_data_sizes()
                self.data_size += subtree.data_size
            return self.data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if (self._subtrees == [] and self.data_size > 0) and \
                (destination._subtrees != []
                 or destination.data_size == 0):
            parent = self._parent_tree
            parent._subtrees.remove(self)
            if parent._subtrees == []:
                parent.data_size = 0
            destination._subtrees.append(self)
            self._parent_tree = destination
            while parent._parent_tree is not None:
                parent = parent._parent_tree
            parent.update_data_sizes()
            parent._helper_close_empty()
        else:
            pass

    def _helper_close_empty(self) -> None:
        if self.data_size == 0:
            self._expanded = False
        elif self.data_size > 0 and self._subtrees == []:
            pass
        else:
            for subtree in self._subtrees:
                subtree._helper_close_empty()

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if self.is_empty():
            self.data_size = 0
        elif self._subtrees != []:
            pass
        else:
            change = self.data_size * factor
            if change < 0:
                new_change = abs(change)
                new_change = math.ceil(new_change)
                change = -new_change
            final = self.data_size + math.ceil(change)
            if final < 1:
                final = 1
            self.data_size = final
    # TODO: (Task 5) Write the methods expand, expand_all, collapse, and
    # TODO: collapse_all, and add the displayed-tree functionality to the
    # TODO: methods from Tasks 2 and 3

    def expand(self) -> None:
        """expend the selected folder into sub file or folder"""
        if self.is_empty():
            pass
        elif self._subtrees == []:
            pass
        else:
            self._expanded = True

    def collapse(self) -> None:
        """collapse this subtree by unexpand its parent tree """
        if self.is_empty():
            self._expanded = False
        elif self._parent_tree is None and self._expanded is True:
            self._expanded = False
        elif self._parent_tree is None:
            pass
        else:
            parent = self._parent_tree
            parent._helper_collapse()

    def _helper_collapse(self) -> None:
        if self.is_empty():
            self._expanded = False
        else:
            self._expanded = False
            for subtree in self._subtrees:
                subtree._helper_collapse()

    def expand_all(self) -> None:
        """expend the corresponding tree into leaves in this"""
        if self.is_empty():
            pass
        elif self._subtrees == []:
            pass
        else:
            self._expanded = True
            for subtree in self._subtrees:
                subtree.expand_all()

    def collapse_all(self) -> None:
        """collapse every thing into the root of the tree"""
        if self.is_empty():
            self._expanded = False
        elif self._parent_tree is None and self._expanded is True:
            self._expanded = False
        elif self._parent_tree is None:
            pass
        else:
            parent = self._parent_tree
            while parent is not None:
                parent.collapse()
                parent = parent._parent_tree
    # Methods for the string representation

    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.

        Remember that you should recursively go through the file system
        and create new FileSystemTree objects for each file and folder
        encountered.

        Also remember to make good use of the superclass constructor!
        TODO: (Task 1) Implement the initializer
        """
        size = os.path.getsize(path)
        name = os.path.basename(path)
        if os.path.isdir(path):
            subtrees = []
            f = os.listdir(path)
            for file in f:
                subtrees.append(FileSystemTree(os.path.join(path, file)))
            TMTree.__init__(self, name, subtrees)
        else:
            TMTree.__init__(self, name, [], size)
    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


def _helper_get_most_closet(result: List[TMTree],
                            pos: Tuple[int, int]) -> Union[bool, TMTree]:
    for p2 in result:
        if p2.rect[0] + p2.rect[2] == pos[0] and p2.rect[1] + \
                p2.rect[3] == pos[1]:
            return p2
    return False


def _helper_get_secondary_closet(result: List[TMTree],
                                 pos: Tuple[int, int]) -> Optional[TMTree]:
    for p2 in result:
        if p2.rect[0] + p2.rect[2] == pos[0] or p2.rect[1] + \
                p2.rect[3] == pos[1]:
            return p2
    return None


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
