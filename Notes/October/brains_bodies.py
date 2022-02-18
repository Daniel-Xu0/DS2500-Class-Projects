slack'''
Daniel Xu
October 5th, 2021
Professor Park
In-Class Notes: How Brains and Bodies Relate
'''
import pandas as pd
import matplotlib.pyplot as plt

brain_body = pd.read_csv('brain_body.csv')
brain_body['body_kg'] = brain_body['body_gm'] / 10000
print(brain_body.head(10))

plt.bar(brain_body.Species, brain_body.brain_gm)
plt.xticks(rotation = 'vertical')
plt.title("Brain Mass")
plt.ylabel("Brain mass (g)")
plt.grid()
plt.show()

brain_body['brain_body_ratio'] = brain_body.brain_gm / brain_body.body_kg
brain_body = brain_body.sort_values(by = 'brain_body_ratio', ascending = False)
brain_body.head(10)