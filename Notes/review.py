#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 14:40:03 2021

@author: asianinvasion
"""

def sorted_ints(string):
    lst = string.split()
    lst1 = list(map(int, lst))
    lst1 = sorted(lst1)
    return lst1


if __name__ == "__main__":
    string = '1 98 4 10 12'
    print(sorted_ints(string))