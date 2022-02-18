"""
Daniel Xu
Measuring Political Bias
In Class Notes - Prof. Park
October 15th, 2021
"""

import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob



#%%
def read_tweets(filename):
    '''
    Function: read_tweet_csv
    Parameters: name of .csv file (string)
    Returns: list of tweet text (strings)
    '''
    with open(filename, encoding = 'utf-8') as infile:
        tweets = infile.readlines()
        tweets = [tweet.strip() for tweet in tweets]
    return tweets


#%% Filtered Tweets

def score_tweets(tweets, minsub = 0.0, maxsub = 1.0, minpol = -1.0, maxpol = 1.0):
    
    filtered = {}
    for tweet in tweets:    
        pol, sub = TextBlob(tweet).sentiment
        if minpol <= pol <= maxpol and minsub <= sub <= maxsub:
            filtered[tweet] = (pol, sub)
            
    return filtered
    
#%% Polarity vs. Subjectivity


def polarity_vs_subjectivity(scored_tweets, title = '', marker = 'black'):
    
    scores = scored_tweets.values()
    polarity = [x[0] for x in scores]
    subjectivity = [x[1] for x in scores]
    
    fig = plt.figure(figsize = (10,10), dpi = 100)
    plt.xlabel('Subjectivity')
    plt.ylabel('Polarity')
    plt.title(title + ': Sentiment Analysis')
    
    sns.scatterplot(x = subjectivity, y = polarity, s = 3, color = marker)
    sns.kdeplot(x = subjectivity, y = polarity, color = 'black')
    plt.show()
    
def main():
    
    trump_tweets = read_tweets('hastag_donaldtrump.csv')
    scored_trump_tweets = score_tweets(trump_tweets)
    polarity_vs_subjectivity(scored_trump_tweets, title = 'Trump', marker = 'red')
    
    biden_tweets = read_tweets('hastag_joebiden.csv')
    scored_biden_tweets = score_tweets(biden_tweets)
    polarity_vs_subjectivity(scored_biden_tweets, title = 'Biden', marker = 'blue')
    
if __name__ == '__main__':
    main()
    
    