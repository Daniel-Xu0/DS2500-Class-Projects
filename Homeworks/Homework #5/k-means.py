"""
Daniel Xu
November 16th, 2021
Homework #5: K-Nearest Neighbor Classification
DS 2500 - Professor Park
"""

import pandas as pd
import seaborn as sns
import csv

"""
Dataset Used: 
    Speaker Accents - 
    https://archive.ics.uci.edu/ml/datasets/Speaker+Accent+Recognition
"""

#%% 

class DataSet:
    
    def __init__(self, filename):
        # Constructor
        self.df = pd.read_csv(filename)
        
    def __repr__(self):
        print_str = "Analyzing data... these are the column names of your dataframe: "
        for column in self.df.columns:
            print_str += column + ', '

        return print_str[:-2]
        
    
        








#%% Main

if __name__ == "__main__":
    
    accents = DataSet('accent_data.csv')
    print(accents)
    
    