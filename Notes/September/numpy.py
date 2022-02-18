"""
DS2500
Spring 2021
Sample code from class --  gnerating an image w/numpy
"""


import random
import numpy as np
import matplotlib.pyplot as plt

DIMEN = 500

image = np.zeros((DIMEN, DIMEN, 3), dtype = int)
# Zeros is a function of numpy that fills the array with 0.0 float balues
# dtype changes all the 0.0 float values into integers

for i in range(DIMEN):
    for j in range(DIMEN):
        red  = i * j % 256
        green = (i*i - j*j) % 256
        blue = (i*i + j*j) % 256
        image[i][j] = [red, green, blue]
        
print(image)
plt.figure(figsize = (10,10))
plt.imshow(image, interpolation = 'none')