#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 16:50:20 2016

@author: karl
"""
import heapq
import timeit
##Read txt file and put in in a dict form vertex: edge
with open('median.txt') as f:
    data = f.read().splitlines()

data = [int(line) for line in data]
#%%
def _heappush_max(heap, item):
    heap.append(item)
    heapq._siftdown_max(heap, 0, len(heap)-1)
def _heappop_max(heap):
    """Maxheap version of a heappop."""
    lastelt = heap.pop()  # raises appropriate IndexError if heap is empty
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        heapq._siftup_max(heap, 0)
        return returnitem
    return lastelt    

#%%
def funcMedianMaintenance():
    heapLow = []
    heapHigh = []
    sizeLow = 0
    sizeHigh = 0
    medianList = []
    
    for i,element in enumerate(data):
        lowCase = False
        highCase = False
        if i== 0:
            heapLow.append(element)
            sizeLow += 1
        else:
            if (element < heapLow[0]):
                _heappush_max(heapLow, element)
                sizeLow += 1
            elif (element > heapLow[0]):
                heapq.heappush(heapHigh, element)
                sizeHigh += 1
                
            if ((sizeLow-sizeHigh) > 1):
                heapq.heappush(heapHigh, _heappop_max(heapLow))
                lowCase = True
            elif ((sizeHigh - sizeLow) > 1):
                _heappush_max(heapLow, heapq.heappop(heapHigh))
                highCase = True
                
            if lowCase:
                sizeLow -= 1
                sizeHigh += 1
            elif highCase:
                sizeHigh -= 1
                sizeLow += 1
        if len(heapLow) >= len(heapHigh):
            medianList.append(heapLow[0])
        else:
            medianList.append(heapHigh[0])
    return medianList

timeit.timeit(funcMedianMaintenance())
#def median(lst):
#    sortedLst = sorted(lst)
#    lstLen = len(lst)
#    index = (lstLen - 1) // 2
#
#    if (lstLen % 2):
#        return sortedLst[index]
#    else:
#        return sortedLst[index]
#
#medianTest=[]
#for i in range(1, 1000):
#    medianTest.append(median(data[:i]))