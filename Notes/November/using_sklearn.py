"""
Daniel Xu
November 11th, 2021
DS 2500 - SciKit Learn
Prof. Raichlin
"""

from sklearn import metrics

#%%

# Constants
C = 'Cat'
F = 'Fish'
H = 'Hen'

# True Values
actual = [C,C,C,C,C,C, F,F,F,F,F,F,F,F,F,F, H,H,H,H,H,H,H,H,H]
# Predicted Values
predicted = [C,C,C,C,H,F, C,C,C,C,C,C,H,H,F,F, C,C,C,H,H,H,H,H,H]

# Print the confusion matrix
matrix = metrics.confusion_matrix(actual, predicted)
print("Confusion Matrix:\n", matrix)

# Print the precision and recall, among other metrics
report = metrics.classification_report(actual, predicted, digits = 3, output_dict = True)
print(report, '\n')
print(report['accuracy'])

report = metrics.classification_report(actual, predicted, digits = 3)
print(report)
