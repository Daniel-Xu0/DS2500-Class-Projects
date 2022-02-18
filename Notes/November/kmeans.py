#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 17:19:19 2021

@author: rachlin
"""

import pandas as pd
import csv
import random as rnd
import copy
import seaborn as sns 
import matplotlib.pyplot as plt
from collections import defaultdict


def read_data(filename):
    """ Read file into attributes data and list of classes """
    data = []
    classes = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # Skip header
        for row in reader:
            data.append(tuple(float(val) for val in row[:4]))
            classes.append(row[4])
    return data, classes


def pick_initial_centroids(data, k):
    """ Pick k random data points as initial centroids """
    return rnd.sample(data, k)


def euclidean(p1, p2):
    """ Euclidean distance measure """
    return sum([(u-v) ** 2 for u, v in zip(p1, p2)]) ** .5


def closest(centroids, point, dfunc):
    """ Determine closest centroid for a given point 
    using the specified distance function """
    nearest = 0
    nearest_dist = dfunc(centroids[0], point)
    for i in range(1, len(centroids)):
        dist = dfunc(centroids[i], point)
        if dist < nearest_dist:
            nearest = i
            nearest_dist = dist
    return nearest


def find_closest_centroid(centroids, data, dfunc):
    """ For each data point find closest centroid.
    Return dictionary (centroid # -> list of points) """    
    cdict = defaultdict(list)                   
    for point in data:
        c = closest(centroids, point, dfunc)
        cdict[c].append(point)
    return cdict


def adjust_centroids(cdict):
    """ Adjust centroids by taking the attribute mean 
    of all points closest to each centroid """
    adjusted = []
    for centroid in cdict:
        pts = cdict[centroid]
        df = pd.DataFrame(pts)
        centroid = list(df.mean(axis=0))
        adjusted.append(centroid)
    return adjusted
        
def visualize(centroids, data):
    """ Visualize data and associated centroids """  
    df = pd.DataFrame(data)
    df['cluster'] = [closest(centroids, point, euclidean) for point in data]
    sns.pairplot(df, hue = 'cluster', palette = 'tab10')
    plt.show()
    
    
def kmeans_cluster(data, k):
    """ Use k-means clustering to identify k centroids for the data """
    # Pick random centroids
    centroids = pick_initial_centroids(data,k)
    
    # Find nearest centroid for each data point, make distance function 
    # a parameter to allow for different distance calculations in the future
    cdict = find_closest_centroid(centroids, data, euclidean)
    
    # Adjust centroids
    new_centroids = adjust_centroids(cdict)
    while centroids != new_centroids:
        centroids = copy.deepcopy(new_centroids)
        cdict = find_closest_centroid(centroids, data, euclidean)
        new_centroids = adjust_centroids(cdict)
    
    # Return final centroids
    return centroids


def wcss(centroids, data):
    """ Compute within-cluster sum of squares """
    wcss_total = 0.0
    for pt in data:
        c = closest(centroids, pt, euclidean)
        dsquared = euclidean(centroids[c], pt) ** 2
        wcss_total += dsquared
    return wcss_total


def visualize_wcss(data, kmin=1, kmax=10):
    """ Plot wcss as a function of k """

    # Compute wcss for each k value
    wvals = []

    for k in range(kmin, kmax+1):
        centroids = kmeans_cluster(data, k)
        w = wcss(centroids, data)
        wvals.append(w)
    
        
    # Display the plot
    plt.figure(figsize=(8,8))
    plt.scatter(range(kmin,kmax+1), wvals, marker='X', c='r')    
    plt.plot(range(kmin, kmax+1), wvals)
    plt.xlabel("k")
    plt.ylabel("wcss")
    plt.title('Finding optimal k using WCSS')
    plt.show()
       
    
def main():
    
    # Read data: split out the raw data from the categories
    data, classes = read_data('iris.csv')
    print(data)
    
    # Find clusters
    centroids = kmeans_cluster(data, k = 3)
    print(centroids)
    
    # Visualize the clusters
    visualize(centroids, data)
    
    # visualize wcss as a function of k
    visualize_wcss(data)


if __name__ == '__main__':
    main()
    
    
    
    
    