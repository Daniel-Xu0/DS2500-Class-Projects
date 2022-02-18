"""
DS 2500: Intermediate Programming with Data
Module: numpy (array-based programming)
File: lists_as_arrays.py
"""

#%% Allocating a list

L = []
L = [1,2,3]
L = [i for i in range(10000000)]
L = [0] * 1000000

L = ['a', [1,2,3], 55, True, (5,6)] # mixed types
L = list('abcdefghij')

#%% Indexing
L[0]
L[-1]
L[:3]
L[3:]

L[2:4]

L[1] = 'x'

#%%  Allocate a 2-D array using lists

twod = [[1,2,3], [4,5,6], [7,8,9]]
print(twod[0][1])
print(twod[2][0])

#%% Iterating over a list

# One dimensional

L = [100, 200, 300]

for value in L:
    print(value)
    
for idx in range(len(L)):
    print(idx, L[idx])

for idx, value in enumerate(L):
    print(idx, value)
    
# Two dimensions (Let's sum the values in the two-d array)
total = 0
for row in twod:
    for value in row:
        total += value
print(total)

#%% Copying lists (shallow vs deep)

A = [1,2,3]
B = A
B[1] = 99
print('A', A)
print('B', B)

# What went wrong? A also changed with B
# We need a deep copy

A = [1,2,3]
B = A[:]
B[1] = 99
print('A', A)
print('B', B)

#%% With higher-dimensions, this becomes clumsier
twod = [[1,2,3], [4,5,6], [7,8,9]]

twod_copy = twod[:]

twod_copy[1][1] = 99
twod_copy[0] = [7,7,7] # But this works, why
print(twod)
print(twod_copy)

#%% Deep copy of multi-dimensional lsits
# Double all the values (a bit clumsy!)

import copy
twod = [[1,2,3], [4,5,6], [7,8,9]]

double = copy.deepcopy(twod) # create a deep copy

for i in range(3):
    for j in range(30):
        double[i, j] = twod[i][j] * 2


