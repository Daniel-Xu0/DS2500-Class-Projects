"""
Tuesday September 28th, 2021
DS2500 - In-Class Notes: Seaborn
Daniel Xu
"""

import matplotlib.pyplot as plt
import seaborn as sns
#Anything you can do in seaborns, you can do in matplotlib

#Built in seaborn datasets
sns.get_dataset_names()

"""
iris = sns.load_dataset('iris')
print(iris)
#Creates a huge mega-graph showing the relationships between all pairs of variables
#in the dataset
sns.pairplot(iris, hue = 'species')

geyser = sns.load_dataset('geyser')
print(geyser)
#Bi-variate data
sns.jointplot(x = 'waiting', y = 'duration', data = geyser, hue  = 'kind')
"""

plt.figure(figsize = (0,0))
sns.regplot(x = 'waiting', y = 'duration')

titanic = sns.load_dataset('titanic')
# sns.displot(titanic['age'])

#%% Swarm Plots
plt.dfigure(figsize = (0,0))
plt.title("Age distribution by class")
sns.boxplot(x = 'pclass', y = 'age')

titanic[['survived', 'sex']].groupby('sex').mean()