#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 10:43:54 2016

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

def read(lines):
    dict = {}
    for i in range(len(lines)):
        lines[i] = lines[i].split("\t")
        del lines[i][-1]
        vertex = int(lines[i].pop(0))
        a=[(int(line.split(',')[0]), int(line.split(',')[1])) for line in lines[i]]
        dict[vertex] = a
    return dict

#%%
##Read txt file and put in in a dict form vertex: edge
with open('dijkstra.txt') as f:
    lines = f.read().splitlines() 
dictGraph = read(lines)

def dijkstra(dictGraph, start, end):
    #init
    listVisited = []
    dictScore = {}
    for vertex in dictGraph.keys():
        if vertex != start:
            dictScore[vertex] = 1000000
        else: 
            listVisited.append(vertex)
            dictScore[vertex] = 0
    while (len(listVisited) < len(dictGraph)):
        shortestVertexStart, shortestVertexEnd, weight = shortestEdge(listVisited, dictGraph, dictScore)
        listVisited.append(shortestVertexEnd)
        dictScore[shortestVertexEnd] = weight
    return listVisited, dictScore
    
    
def shortestEdge(listVisited, dictGraph, dictScore):
    minWeight = 1000000
    for vertex in listVisited:
        for edge in dictGraph[vertex]:
            if edge[0] not in listVisited:
                if edge[1] + dictScore[vertex] <= minWeight:
                    minWeight = edge[1] + dictScore[vertex]
                    shortestVertexEnd = edge[0]
                    shortestVertexStart = vertex
    return shortestVertexStart, shortestVertexEnd, minWeight


a = dijkstra(dictGraph, 1, -2)[1]
c = np.sort(np.array(a.values()))
for i in [7,37,59,82,99,115,133,165,188,197]:
    print(a[i])