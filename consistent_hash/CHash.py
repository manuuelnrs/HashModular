#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@noemail.com>
#
# Distributed under terms of the MIT license.

"""
A minimal consistent hash implementation
"""
from bisect import bisect_left

from HashScheme import HashScheme
import hashlib

class CHash(HashScheme):
    def __init__(self):
        self.__scheme_name = 'Consistent_Hash'
        self.nodes = {}

    def __get_hash(self, value):
        """
        Calculates an initial hash using md5.
        """
        return int(hashlib.md5(value.encode()).hexdigest(),16) % 10000

    def get_name(self):
        return self.__scheme_name

    def dump(self):
        """
        Prints information about the hash generator
        """
        for k in self.nodes.keys():
            print ("Node: {0} hash: {1}".format(self.nodes[k], k))

    def add_node(self, new_node):
        """
        Adds a new node to the ring.
        """
        hash_value = self.__get_hash(new_node)
        if hash_value not in self.nodes.keys():
            self.nodes[hash_value] = new_node
            return 0
        return 1

    def remove_node(self, node):
        """
        Removes a node from the ring
        """
        hash_value = self.__get_hash(node)
        if hash_value in self.nodes.keys():
            del self.nodes[hash_value]
            return 0
        return 1

    def hash(self, value):
        """
        Given a value, find its location in the consistent hash ring.
        """
        if len(self.nodes.keys()) == 0:
            return None

        hash_value = self.__get_hash(value)

        """
        Get the list of elements in the order in which they appear in the ring.
        """
        sorted_nodes = sorted(self.nodes.keys())
        r = len(sorted_nodes) - 1
        l = 0

        if hash_value < sorted_nodes[0] or hash_value >= sorted_nodes[r]:
            return self.nodes[sorted_nodes[r]]

        """
        Binary search the right spot for the given value in the hash ring.
        """
        found_index = bisect_left(sorted_nodes, hash_value)
        if sorted_nodes[found_index] != hash_value:
            found_index -= 1

        return self.nodes[sorted_nodes[found_index]]

