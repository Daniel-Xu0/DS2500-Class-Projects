"""
Daniel Xu
October 1st, 2021
DS2500 - Park
In Class Notes: Inverse Distance Weighting
"""

import pandas as pd

# data_dict = {'place': ['A', 'B', 'C', 'D', 'E'], 
#              'dist' : [2, 15, 20, 1000, 1500],
#              'temp' : [30.0, 23.0, 28.0, 68.0, 79.0]}

data_dict = {'place': ['A', 'B', 'C', 'D', 'E'] * 2, 
             'dist' : [2, 15, 20, 1000, 1500] * 2,
             'temp' : [30.0, 23.0, 28.0, 68.0, 79.0] + [34.0, 41.0, 50.0, 68.0, 82.0],
             'day': [1] * 5 + [2] * 5}

data = pd.DataFrame(data_dict)
print(data)

#Create new column which calculates inverted distance
p = 1
data['inv_dist'] = 1 / data['dist'] ** p

#Create new column for weighted value
data['weighted'] = data.temp * data.inv_dist
print(data)


#Grouping dataframe by the day to easily sum the weights of each group
data.groupby('day')
list(data.groupby('day').weighted)

inv_weight = data.groupby('day').weighted.sum() / data.groupby('day').inv_dist.sum()
print(inv_weight)

grouped = data.groupby('day').sum()[['inv_dist', 'weighted']]
print(grouped)

grouped['final'] = grouped.weighted / grouped.inv_dist
print(grouped)