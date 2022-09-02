#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@noemail.com>
#
# Distributed under terms of the MIT license.

from CHash import *
from ModHash import *
from Store import *
"""
Creates a Store that is managed using a consistent hash.

We store a bunch of words in the datastore, then remove one node from the store
and then add it back.
"""


def read_words(fname):
  """
  Just read a bunch of words from a file.
  """
  result = []
  with open(fname, 'r') as f:
    for word in f:
      word = word.split('/')[0]
      word = word.strip()
      result.append(word)

  return result


def run(words):
  """
  We create an object representing the hash scheme that we are willing to use.
  The hash object is then passed to the Store constructor. When adding elements
  to the store, the selected hash scheme is used to determine where to place
  the records.
  """
  #my_hash = CHash()
  my_hash = ModHash()
  my_store = Store(my_hash)
  
  
  """
  Add three nodes to the Store
  """
  my_store.add_node("Node 1")
  my_store.add_node("Node 2")
  my_store.add_node("Node 3")
  
  my_store.dump()
  

  """
  Save all words in the Store
  """
  for word in words:
      my_store.add_resource(word)
  
  my_store.dump()


  """
  Remove one node from the Store. Stored objects need to be migrated to the
  remaining nodes.
  """
  print(" ----REMOVIENDO NODO 1........")
  my_store.remove_node("Node 1")
  my_store.dump()


  """
  Add the node back to the Store. Objects need to be migrated to conform to the
  Hash scheme.
  """
  print(" ----AÑADIENDO NODO 1........")
  my_store.add_node("Node 1")
  my_store.dump()

if __name__ == '__main__':

  words = read_words('C:\\Users\\ASUS\\Downloads\\A_SEMESTRE2023_I\\SD\HashModular\\HashModular\\consistent_hash\\words_alpha.txt')
  words = words[:100]

  run(words)
