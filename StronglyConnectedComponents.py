#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 18:23:54 2016

@author: karl
"""

import pandas as pd
import numpy as np
import random
import copy
import sys
import resource
from collections import Counter
import itertools
## improving recusion depth
sys.setrecursionlimit(800000)
resource.setrlimit(resource.RLIMIT_STACK, (2**21, 2**22))

# creating Graph data structure
from collections import defaultdict
#
class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._graph and node2 in self._graph[node1]

    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))
        
#
def readOrder(lines, dictF):
    for i in range(len(lines)):
        a = lines[i].split(" ")
        if len(a) > 2: ## depend if there is a blank space after the second figure or not
            a.pop()
        lines[i] = (dictF[int(a[0])], dictF[int(a[1])])
        
def readInverseOrder(lines):
    for i in range(len(lines)):
        a = lines[i].split(" ")
        if len(a) > 2: ## depend if there is a blank space after the second figure or not
            a.pop()
        lines[i] = (int(a[1]), int(a[0]))

#

def DFS(graph, dictVisited, startVertex, t, s, dictLeader, dictF):
    dictVisited[startVertex] = True
    dictLeader[startVertex] = s
    for endingVertex in graph._graph[startVertex]:
        if dictVisited[endingVertex] == False:
            t = DFS(graph, dictVisited, endingVertex, t, s, dictLeader, dictF)
    t += 1
    dictF[startVertex] = t
    return t
    
#
def DFSLoop(graph):
    t = 0 # number of nodes processed so fare
    s = None
    dictVisited = {}
    dictLeader = {}
    dictF = {}
    for g in range(1, nbOfNode + 1):
        dictVisited[g] = False
    #Assume node labelled 1 to n
    for i in range(nbOfNode, 0, -1):
        if not dictVisited[i]:
            s = i
            t = DFS(graph, dictVisited, i, t, s, dictLeader, dictF)
    return dictLeader, dictF
    
#%%
##Read txt file and put in in a dict form vertex: edge
with open('data.txt') as f:
    lines = f.read().splitlines() 
readInverseOrder(lines)
nbOfNode = 875714
graph = Graph(lines, directed=True)    
del lines
#%%
leaderReverse, fReverse = DFSLoop(graph)
del graph
#%%
##Read txt file and put in in a dict form vertex: edge
with open('data.txt') as f:
    linesOrder = f.read().splitlines() 
readOrder(linesOrder, fReverse)
nbOfNode = 875714
graph = Graph(linesOrder, directed=True)
#%%
leaderOrder, fOrder = DFSLoop(graph)
#%%
c = Counter(leaderOrder.values())
t = c.values()
t.sort()
t[::-1][:5] # result here
    
    