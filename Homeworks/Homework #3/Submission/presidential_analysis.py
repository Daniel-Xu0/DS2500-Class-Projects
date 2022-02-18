"""
Daniel Xu
Professor Park
October 16th, 2021
Homework #3: Presidential Sentiment Analysis

----------------------------------------------------------------------
What can a President's inaugural address tell us about the political 
climate they served under?
----------------------------------------------------------------------
"""
import wordcloud as wc
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
from collections import Counter
from pathlib import Path
from nltk.corpus import stopwords
from textblob import TextBlob

BIDEN = 'biden_address.txt'
OBAMA = 'obama_address.txt'
CARTER = 'carter_address.txt'

TRUMP = 'trump_address.txt'
BUSH = 'bush_address.txt'
REAGAN = 'reagan_address.txt'

SENTIMENT_VALUES = 'wordwithStrength.txt'
NAMES = ['Biden', 'Obama', 'Carter', 'Trump', 'Bush', 'Reagan']

#%% Part 1: Getting Inaugural Addresses

def read_text(filename):
    '''
    Function: Read in a txt file
    Parameters: filename
    Return: the text as a string
    '''
    text = Path(filename).read_text()
    text = text.replace('\n', '')
    
    return text

#%% Part 2: Generating Word Clouds

def word_cloud(text):
    '''
    Function: Generate a wordcloud from a piece of text
    Parameters: text/passage (str)
    Return: wordcloud
    '''
    
    cloud = wc.WordCloud().generate(text)
    # plt.imshow(cloud)
    # plt.axis('off')
    return cloud

def compare_clouds(texts, titles):
    '''
    Function: Create a wordcloud array to visualize/compare all 6 wordclouds
    Parameters: 6 different wordclouds, 6 different titles (str)
    Return: Array figure
    '''
    fig = plt.figure(figsize = (9.5,4), dpi = 200)
    
    for i in range(len(texts)):
        fig.add_subplot(2,3,i+1)
        plt.imshow(word_cloud(texts[i]))
        plt.title(titles[i], fontdict = {'family': 'serif', 'fontsize' : 18})
        plt.axis('off')
    
    plt.show()

#%% Part 3: Sentiment Analysis

def sentiment_analysis(text):
    '''
    Function: conduct a sentiment analysis for the given text
    Parameters: text (str), list of words and the positive/negative value
                associated with them
    Return: A sentiment score for the text
    '''

    #Unpack list of words and their sentiment values into a dictionary
    # https://github.com/hitesh915/sentimentstrength/blob/master/wordwithStrength.txt
    # was resource used to obtain sentiment scores
    word_sentiments = {}
    with open(SENTIMENT_VALUES, 'r') as infile:
        for line in infile:
            word, sentiment = line.split()
            word_sentiments[word] = float(sentiment)
            
    #split text into sentences
    sentences = text.split('.')
    
    #Get individual sentiment values for each sentence
    sentiments = []
    for sentence in sentences:
        #Adding up sentiment value for each word to get total sentiment value
        #for the sentence
        sentence_sentiment = 0
        for word in sentence:
            #Check if the word has a sentiment value associated with it, if so
            #add the sentiment value to the counter
            if word in word_sentiments.keys():
                sentence_sentiment += word_sentiments[word]
        sentiments.append(float(sentence_sentiment))

    return sentiments

def compare_sentiments(texts, xaxis, colors):
    '''
    Function: compare sentiment values between each President's speech
    Parameters: list of texts (list)
    Return: a boxplot visualization of sentiment scores 
    '''
    #Get list of sentence sentiment scores from each speech
    sentiment_scores = [sentiment_analysis(text) for text in texts]
    
    #Create a boxplot to compare the scores
    box = plt.boxplot(sentiment_scores, patch_artist = True)
    
    #Change box colors to political party colors
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
        
    plt.xticks([i+1 for i in range(len(xaxis))], xaxis)
    plt.xlabel("President")
    plt.ylabel("Sentiment Score per Sentence")
    plt.title("Sentiment Analysis of Inaugural Speeches")
        
    plt.show()
    
#%% Part 4: Most Common Words

def filter_words(text):
    '''
    Function: Clean the speech, get rid of small, unimportant words and 
              punctuation
    Parameters: speech text (str)
    Return: a cleaned version of the text (str)
    '''
    
    #Regular expression that stands for punctuation
    punctuation = "[^\w\s]"
    
    text = re.sub(punctuation, ' ' , text)
    words = text.split()
    
    #Use nltk module to get a list of stopwords to exclude from text
    #these would be words like 'it', 'your', 'the', etc.
    stop_words = set(stopwords.words('english'))

    word_lst = [word.lower() for word in words if word.lower() not in stop_words]
    
    ''' I didn't like how generation and generations were being counted as 
        two words so I looked for a way to turn plural nouns into their 
        singular counterparts. The next couple lines of code should work,
        but anaconda isn't letting me download the pattern package :(
    '''
    # from pattern.text.en import singularize
    # singularized_word_lst = [singularize(word) for word in word_lst]
    
    return word_lst

def count_common_words(word_lst, k):
    '''
    Function: Create a set of the most common words spoken in the speech
    Parameters: List of texts (list), number of most common words to be taken
                from each speech
    Return: set of most common words
    '''
    
    #User counter module to count and find the most common words spoken in text
    speech_count = Counter(word_lst)
    common_words = speech_count.most_common(k)
    
    return common_words


def count_overlap(word_lst1, word_lst2, k):
    '''
    Function: Count the overlapping words between two speeches
    Parameters: list of words and their # of occurreces from speech 1 
                and speech 2 (list of tuples), # of most common words to count
                overlap from (int)
    Return: a list of overlapping words from the two speeches
    '''
    common_word_freq1 = count_common_words(word_lst1, k)
    common_word_freq2 = count_common_words(word_lst2, k)

    #Will hold overlapping words and occurrences for speech 1 and speech 2
    overlap_words1 = []
    overlap_words2 = []
    
    #Turn list of common words from speech 2 into a dictionary
    word_freq_dict = dict(common_word_freq2)
    
    #Iterate through list of common words tuples
    for word_freq1, word_freq2 in zip(common_word_freq1, common_word_freq2):
        #If a word in the first speech is also in the second speech
        if word_freq1[0] in word_freq_dict.keys():
            #then append that word and its frequency to overlap list 1 and 2
            overlap_words1.append(word_freq1)
            overlap_words2.append((word_freq1[0], word_freq_dict[word_freq1[0]]))
            
    return overlap_words1, overlap_words2

def plot_overlap(words_from_speeches, k, axis_labels):
    """
    Function: Create a heat map of the most spoken words in every speech
    Parameters: list of words fromn each speech nested list of strings, 
                # of most common words to count overlap from (int)
    Return: A heat map comparing the most common words spoken in the two speeches 
    """
    #Find k most common words and their frequencies from the list of speeches
    speeches_word_freq = [count_common_words(speech, k) for speech 
                          in words_from_speeches]
    
    #Generate an array that will hold the contents of the heatmap
    array_dimen = len(speeches_word_freq)
    sim_array = np.zeros((array_dimen, array_dimen))
    
    #Get a list of just the top words spoken in each speech, no frequencies
    common_words_lst = []
    for speech in speeches_word_freq:
        common_words = [word for word, freq in speech]
        common_words_lst.append(common_words)
        
    #Adding one to the designated array value if a word appears in two 
    #respective speeches
    for i in range(len(speeches_word_freq)):
        for j in range(len(speeches_word_freq)):
            for words in common_words_lst[j]:
                if words in common_words_lst[i]:
                    sim_array[i, j] += 1
    
    
    sns.heatmap(sim_array)
    plt.title("Comparing the # of Overlapping Words Between Speeches")
    plt.xticks(ticks = [0.5,1.5,2.5,3.5,4.5,5.5], labels = axis_labels)
    plt.yticks(ticks = [0.5,1.5,2.5,3.5,4.5,5.5], labels = axis_labels,
               rotation = 'horizontal')
    plt.show()
    
#%% Part 5: Other Comparative Measures

def sentence_length(speeches, labels, colors):
    '''
    Function: find the average sentence length of the text
    Parameters: text/passage (str)
    Return: average number of words and characters per sentence (ints)
    '''
    
    for i, speech in enumerate(speeches):
        sentences = speech.split('.')
        num_sentences = len(sentences)
        
        #Find len of each sentence/str in the text which will be the number of 
        #characters in that sentence
        characters = [len(sentence) for sentence in sentences 
                             if len(sentence) > 1]
        char_per_sentence = sum(characters) / num_sentences
        
        #Find len of each sentence after it's been split up into words 
        #This will be the number of words in that sentence
        words = [len(sentence.split()) for sentence in sentences
                              if len(sentence) > 1]
        words_per_sentence = sum(words) / num_sentences
        plt.plot(char_per_sentence, words_per_sentence, 'o', color = colors[i],
                 label = labels[i])
        plt.annotate(labels[i], xy = (char_per_sentence + 1, words_per_sentence))

    plt.title("Sentence Length of Presidential Speeches")
    plt.xlabel("Characters per Sentence")
    plt.ylabel("Words per Sentence")
    plt.show()
    
def unique_words(text_lst):
    '''
    Function: Count the number of unique words used in the text (ie. the word
              only appears once throughout the text)   
    Parameters: Text/passage (str)
    Return: Number of unique words (int)
    '''
    '''
    There was this interesting syntax/function that can find the number of
    unique words in a text by finding all the hapaxes (words that only 
    appear once, but I'm not entirely sure how it works and don't know if it
    gives a correct answer, so I just stuck to what I know)
    https://stackoverflow.com/questions/49218417/counting-distinct-words-in-a-
    speech-using-tagset-in-nltk
    '''
    # words = nltk.FreqDist(text_lst)
    # unique_words = len(words.hapaxes()) / len(text_lst)
    
    unique_words = []
    for word in text_lst:
        if word not in unique_words:
            unique_words.append(word)
    
    unique_pct = (len(unique_words) / len(text_lst)) * 1000
    
    return unique_pct

def score_sentences(text, minsub = 0.0, maxsub = 1.0, minpol = -1.0, maxpol = 1.0):
    '''
    Function: Score each sentence within the text with a polarity and 
              subjectivity rating.
    Parameters: Text (str), subjectivity and polarity ranges (floats).
                0 (objective) to 1 (subjective) for subjectivity,
                -1 (negative) to 1(positive) for polarity
    '''
    sentences = text.split('.')
    sentence_scores = {}
    for sentence in sentences:
        pol, sub = TextBlob(sentence).sentiment
        if minpol <= pol <= maxpol and minsub <= sub <= maxsub:
            sentence_scores[sentence] = (pol, sub)
            
    return sentence_scores

def polarity_subjectivity(speech_list, titles, party_colors, marker = 'black'):
    '''
    Function: Conduct sentiment analysis of the text
    Parameters: text/passage (str)
    Return: a density plot depicting the text's polarity and subjectivity
    '''
    fig = plt.figure(figsize = (18,12), dpi = 100)
    
    for i in range(len(speech_list)):

        scored_sentences = score_sentences(speech_list[i])
        
        scores = scored_sentences.values()
        polarity = [score[0] for score in scores]
        subjectivity = [score[1] for score in scores]
        
        #Polarity v Subjectivity subplot for text1
        fig.add_subplot(2,3,i+1)
        sns.scatterplot(x = subjectivity, y = polarity, s = 15, color = marker)
        sns.kdeplot(x = subjectivity, y = polarity, color = party_colors[i])
        plt.xlabel('Subjectivity')
        plt.ylabel('Polarity')
        plt.title(titles[i] + ': Sentiment Analysis')
        
    plt.show()
    
#Cosine Similarity
def unique_common_words(speech_words_lst, k):
    '''
    Function: create a set of the most common words from each speech
    Paramters: nested list of words spoken from each speech, # of most common
               words to be taken from each speech (int)
    Return: a set of unique common words
    '''
    
    unique_words = set()
    
    for speech in speech_words_lst:
        common_words = count_common_words(speech, k)
        unique_words.update([i for i, j in common_words])

    return unique_words

def vector(unique_words, all_words_lst):
    '''
    Function: create a vector of the most common words
    Parameters: set of unique words to compare to, list of all the words
                spoken in each speech
    Return: vector between unique words and the most spoken words in a speech
    '''
    vector = []
    # Turn set of unique_words back into list since it's easier to work w
    unique_words = list(unique_words)
    
    #Take the list of all words spoken in the text and count the words spoken
    words_freq_lst = [Counter(speech_words) for speech_words in all_words_lst]
    #Take just the words, leave the frequencies
    words_spoken = [words_freq.keys() for words_freq in words_freq_lst]
    
    vector_lst = []
    
    for i, speech in enumerate(words_spoken):
        vector = []
        for unique in unique_words:
            #If one of the unique words is in the list of all words used
            #in the speech, then find that word used in the speech and append
            #it's frequency rate
            if unique in speech:
                vector.append(words_freq_lst[i][unique])
            else:
                vector.append(0)
        
        #Append each of the speeches vector to the vector list
        vector_lst.append(vector)
    
    return vector_lst

def vector_mag(vector):
    
    return sum([i**2 for i in vector]) ** .5

def dot_product(vector1, vector2):

    return sum([i * j  for i, j in zip(vector1, vector2)])

def cosine_similarity(vector1, vector2):
    
    cos_theta = dot_product(vector1, vector2) / (vector_mag(vector1) 
                                                 * vector_mag(vector2))
    return cos_theta

def cos_sim_heatmap(vector_lst, axis_labels, dimensions = 6):

    simarray = np.zeros((dimensions, dimensions), dtype = float)
    
    for i in range(dimensions):
        for j in range(dimensions):
            simarray[i, j] = cosine_similarity(vector_lst[i], vector_lst[j])
    
    sns.heatmap(simarray, vmin = 0.0, cmap = "Blues")
    plt.title("Cosine Similarity Between Each Presidents' Speeches")
    plt.xticks(ticks = [0.5,1.5,2.5,3.5,4.5,5.5], labels = axis_labels)
    plt.yticks(ticks = [0.5,1.5,2.5,3.5,4.5,5.5], labels = axis_labels,
               rotation = 'horizontal')
    
    plt.show()
    
    
#%% Main Function

if __name__ == "__main__":
    
    party_colors = ['royalblue', 'royalblue', 'royalblue', 'firebrick',
                    'firebrick', 'firebrick']
    labels = ["Biden", "Obama", "Carter", "Trump", "Bush", "Reagan"]
    
    ''' Part 1: Reading in Text Files '''

    biden = read_text(BIDEN)
    obama = read_text(OBAMA)
    carter = read_text(CARTER)
    trump = read_text(TRUMP)
    bush = read_text(BUSH)
    reagan = read_text(REAGAN)
    
    TEXTS = [biden, obama, carter, trump, bush, reagan]

    ''' Part 2: Generate WordClouds '''
    

    compare_clouds(TEXTS, labels)
    
    ''' Part 3: Conduct a Sentiment Analysis '''
    
    compare_sentiments(TEXTS, labels, party_colors)
    
    ''' Part 4: Overlapping Words '''
    filtered_speeches = [filter_words(speech) for speech in TEXTS]
    plot_overlap(filtered_speeches, 100, labels)
    
    ''' Part 5: Using Other Comparative Measures '''
    
    #Cosing Similarity
    unique = unique_common_words(filtered_speeches, 50)
    vector_lst = vector(unique, filtered_speeches)
    cos_sim_heatmap(vector_lst, labels)
    
    #Polarity and Subjectivity
    polarity_subjectivity(TEXTS, labels, party_colors)
    
    #Sentence Length
    sentence_length(TEXTS, labels, party_colors)
    
    
    
    
    

    
    
    
    
    
    
