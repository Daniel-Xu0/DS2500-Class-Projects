"""
Daniel Xu
November 16th, 2021
Homework #5: K-Nearest Neighbor Classification
DS 2500 - Professor Park
"""

import pandas as pd
from sklearn import metrics
import matplotlib.pyplot as plt
from collections import Counter

"""
Dataset Used: 
    Speaker Accents - 
    https://archive.ics.uci.edu/ml/datasets/Speaker+Accent+Recognition
"""

#%% K-Folds Cross Validation

def to_dataframe(filename):
    '''
    Function: Read file into dataframe, change index column
    Parameters: filename (str)
    Return: a dataframe
    '''
    # Read in csvfile and make row # and language column the index
    df = pd.read_csv(filename)
    df.set_index([pd.Index([i+1 for i in range(len(df))]), 'language'],
                  inplace = True)
    return df

# Thought this was needed for the homework
# def folds(df, k):
#     '''
#     Function: split data into k-folds
#     Parameters: dataframe, k (integer)
#     Return: k subsets of data from dataframe
    
#     Citation (how to randomly divide dataframe into smaller subsets): 
#     https://stackoverflow.com/questions/54730276/how-to-randomly-split-a-
#     dataframe-into-several-smaller-dataframes
#     '''
#     shuffled = df.sample(frac=1)
#     result = np.array_split(shuffled, k)  
#     return result

def euclidean(p1, p2):
    """ Euclidean distance measure """
    
    return sum([(u-v) ** 2 for u, v in zip(p1, p2)]) ** .5

def compute_distances(data, dfunc):
    """
    Function: For each datapoint, find its distance between every other datapoint
    Parameters: Data (dataframe), distance function
    Return: Return a dictionary of each datapoint's distances
    """
    
    distances = {}
    
    for index, test in data.iterrows():
        distances[index] = []
        for index1, train in data.iterrows():
            # Find distance between every combination of two datapoints; 
            # omitting itself
            if index != index1:
                distance = dfunc(test, train)
                distances[index].append([distance, index1])
                
    return distances

def closest(distances, k):
    """
    Function: Find the k-nearest neighbors to each datapoint
    Parameters: Distances (dictionary), k-neighbors (int)
    Return: k-closest neighbors to each datapoint (sorted dictionary)
    """
    
    nearest_neighbors = {}
    # Sort valuess, find the k-nearest neighbors
    for key, value in distances.items():
        new_distances = sorted(value)
        nearest_neighbors[key] = new_distances[:k]
        
    return nearest_neighbors
        
def classify(nearest_neighbors):
    """
    Function: classify each datapoint by its nearest neighbors
    Parameters: nearest neighbors of each point (dictionary)
    Return: classification of each point
    """
    
    # Create holder lists, estimated will show what our knn algorithm believes
    # each point is. Actual will be what the point's classification actually is.
    projected_class = []
    actual_class = []
    
    for key, value in nearest_neighbors.items():
        actual_class.append(key[1])
        
        neighbor_classes = []
        for neighbors in value:
            neighbor_classes.append(neighbors[1][1])
            
        # Use counter module to find the most common classification of neighbors
        count = Counter(neighbor_classes)
        projected_class.append(count.most_common(1)[0])
        
    return actual_class, projected_class
    
def k_folds_classification(data, dfunc, k):
    """
    Compiler function; classifies each datapoint based on nearest neighbors
    """
    
    distances = compute_distances(data, dfunc)
    nearest_neighbors = closest(distances, k)
    actual_class, projected_class = classify(nearest_neighbors)
    
    return actual_class, projected_class


#%% Measuring Accuracy with Increasing K-Values

def k_accuracy(data, dfunc, kmin, kmax):
    """
    Function: Determine how accurate our classifier is with different k-values
    Parameters:
    Return:
    """
    accuracy = []
    precision = []
    recall = []
    f1_scores = []
    k_values = [k for k in range(kmin, kmax+1)]
    
    for k in range(kmin, kmax+1):
        actual, predicted = k_folds_classification(data, dfunc, k)
        # Remove count of the prediction, leave just the prediction
        predicted = [estimate[0] for estimate in predicted]
        

        # Use sklearn's metrics module to get the accuracy, precision, recall, 
        # and f1-scores
        report = metrics.classification_report(actual, predicted, digits = 3,
                                               output_dict = True)
        print(report)

        accuracy.append(report['accuracy'])
        precision.append(report['weighted avg']['precision'])
        recall.append(report['weighted avg']['recall'])
        f1_scores.append(report['weighted avg']['f1-score'])
        
    fig, axes = plt.subplots(2,2)
    axes[0,0].plot(k_values, accuracy, color = 'orchid')
    axes[0,0].set_title('Accuracy')
    axes[0,1].plot(k_values, precision, color = 'royalblue')
    axes[0,1].set_title('Precision')
    axes[1,0].plot(k_values, recall, color = 'firebrick')
    axes[1,0].set_title('Recall')
    axes[1,1].plot(k_values, f1_scores, color = 'turquoise')
    axes[1,1].set_title('F1-Scores')
    fig.suptitle('Classification Report')

    for ax in axes.flat:
        ax.set(xlabel='K-Value', ylabel = 'Score')
        ax.set_yticks([.75, .8, .85])
        
    for ax in fig.get_axes():
        ax.label_outer()
        
    plt.show()
    
#%% Main

if __name__ == "__main__":
    
    accents = to_dataframe('accent_data.csv')
    k_accuracy(accents, euclidean, 1, 20)
    
    
