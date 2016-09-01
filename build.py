#!/usr/bin/env python
import images
import pprint
import pdb

class Node:

    def __init__(self, letter):
        self.letter = letter
        self.children = {}
        self.output = []
        self.is_root = False
        self.f = None

    def g(self, a):
        """ The goto function
        """
        if a in self.children:
            return self.children[a]
        else:
            if self.is_root:
                return self
            else:
                return None

    def __str__(self):
        if len(self.children) == 0:
            return str(self.letter) + ' = ' + str(self.output)
        s = str(self.letter) + " -> " + str(self.children)
        return s

    def __repr__(self):
        return self.__str__()


def serialise(root):
    """ Takes a search tree and converts it into a JSON representation
        which can later be restored by deserialise
    """
    # Return a JSON representation of the tree
    return ""


def deserialise(str):
    """ Takes a JSON representation of a search tree and
        deserialises it into the tree it represents
    """
    return Node('')


def main(needles):
    """ Build an Aho-Corasick search tree for the provided search strings
        following the algorithm provided in:
        Efficient String Matching: An Aid to Bibliographic Search by
        Alfred Aho and Margaret Corasick, published in
        Communications of the ACM June 1975 Volume 18 Number 7
        http://cr.yp.to/bib/1975/aho.pdf
    """

    #
    # Build a prefix tree (trie) from our search patterns
    #
    root = Node('')
    nodes = [root]
    for needle in needles:
        node = root
        for letter in needle.magic:
            if letter not in node.children:
                node.children[letter] = Node(letter)
            node = node.children[letter]
        node.output = [needle]

    root.is_root = True

    #
    # Algorithm 3
    # Set the base failure case (all nodes of depth one have f=0)
    #
    q = []
    for c in root.children.values():
        c.f = root
        q.append(c)

    #
    # Algorithm 3
    # Derive the failure cases for the rest of the tree
    #
    visited = q
    while len(q) > 0:
        r = q.pop()
        for s in r.children.values():
            q.append(s)
            state = r.f
            while state.g(s.letter) is None:
                state = state.f
            s.f = state.g(s.letter)
            s.output.extend(s.f.output)

    #
    # Not implemented: reworking the tree to
    # replace failure transition (Algorithm 4)
    #

    return root


if __name__ == '__main__':
    # Example usage
    root = main(images.types)
    print(root)
    print("\n************************\n")
    haystack = [1, 2, 3, 255, 216]
    state = root
    for a in haystack:
        while state.g(a) is None:
            state = state.f
        state = state.g(a)
        if state.output:
            print(state.output)
