"""
DS2500
Spring 2021
Sample code from class --  gnerating an image w/numpy
"""


import random
import numpy as np
import matplotlib.pyplot as plt

DIMEN = 1700

image = np.zeros((DIMEN, DIMEN), dtype = int)
# Zeros is a function of numpy that fills the array with 0.0 float balues
# dtype changes all the 0.0 float values into integers

for i in range(DIMEN):
    for j in range(DIMEN):
        image[i,j] = (i * j) % 17 # bin(i*j).count('1')
        
plt.figure(figsize = (10,10))
plt.imshow(image, interpolation = 'none')