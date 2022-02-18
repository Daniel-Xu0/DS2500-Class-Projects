'''
Daniel Xu
October 5th, 2021
Professor Park
In-Class Notes: How Brains and Bodies Relate
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as stats

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
print(brain_body.head(10))

brain_body['log_brain'] = np.log10(brain_body.brain_gm)
brain_body['log_body'] = np.log10(brain_body.body_kg)
sns.regplot(x = brain_body.log_body, y = brain_body.log_brain)
plt.grid()
plt.title('Brain vs Body Weight')

lm = stats.linregress(x = brain_body.log_body, y = brain_body.log_brain)
brain_body['pred_brain'] = lm.slope * brain_body.log_body + lm.intercept
brain_body['enceph'] = brain_body.log_brain - brain_body.pred_brain