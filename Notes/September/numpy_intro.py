"""
DS2500: Intermediate Programming with Data
Module: numpy (array-based programming)
File  : numpy_intro.py

"""


import numpy as np


#%% Create a numpy array from a list


print("A list")
A = [[1,20,3], [400,5,6], [7,8888,9], [0,0,0]]
print(A)

print("\n\nA numpy array")
N = np.array(A)
print(N)



#%% Array properties

def array_props(A):
    print("Array: ")
    print(A)
    print("type:     ", type(A))
    print("dtype:    ", A.dtype)
    print("size:     ", A.size)
    print("itemsize: ", A.itemsize)
    print("shape:    ", A.shape)
    print("ndim:     ", A.ndim)


array_props(N)

#%% Initializing

A = np.zeros((5,10), dtype=int)
print(A)

B = np.ones((2,2), dtype=float)
print(B)
import numpy as no
C = np.full((3,3), 3.14)
print(C)

D = np.arange(5)
print(D)


E = np.arange(1,101).reshape(10,10)
print(E)


F = np.linspace(0.0, 10.0, num=5)
print(F)


G = np.empty((8,8), dtype=float) # Slightly faster allocation but value is unpredictable
print(G)


# From a function

def f(x,y):
    return x * y

MT = np.fromfunction(f, (11,11), dtype=int)
print(MT)


# This also works (using lambda functions)
MT = np.fromfunction(lambda x,y: x*y, (11,11), dtype=int)
print(MT)

import numpy as np
# This also works (using transpositions!)
A = np.array([[i]*11 for i in range(0,11)])
#Transpose
print(A)
B = A.T
print(B)
MT = A * B
print(MT)



#%% Array-oriented processing

X = 2 * MT
print(X)

X[0,0] = 99 # or X[0][0] = 99
print(X)

X += 1
print(X)

print("Original")
print(MT)

print(MT>50)

 

#%% Random numbers

import random as rnd

# Doesn't work
R = np.full((5,5), rnd.uniform(-1,1))
#print(R)


# Works
R = np.random.uniform(-1, 1, (5,5))
print(R)

#%% Grades: Aggregations by row, column, or over the whole array
grades = np.random.randint(70,100,size=(10,3), dtype=int)
print(grades)
print(grades.sum())


print("All grades: ", grades.mean())  # sum, min, max, std
print("Mean by test (column): ", grades.mean(axis=0))
print("Mean by student (row): ", grades.mean(axis=1))




