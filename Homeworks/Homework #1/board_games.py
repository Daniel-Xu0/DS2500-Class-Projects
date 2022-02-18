"""
Daniel Xu
DS2500 - HW #1: Board Games
September 26th, 2021
"""

import csv
import math
import matplotlib.pyplot as plt

FILENAME = 'bgg.csv'
MAGE = 'Mage Knight Board Game'

boardgames = {}

def csv_to_dict(filename):
    '''
    Function: 
        Read in a csv file
    Parameters:
        Name of file (string)
    Returns:
        A dictionary of the csv file
    '''
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ",")
        #Read csv file, space out each element whenever there's a comma
        next(csv_reader)
        #Skips headers
        for row in csv_reader:
            #We only want baordgames that can be played by yourself (solo-player)
            if int(row[1]) == 1:
                game_info = {}
                #Create a dictionary to hold variables of each game's info/
                #attributes

                #Puts various game information as the items in the game_info dict.
                #game info variable is key, actual number value is value
                game_info['minplaytime'] = int(row[2])
                game_info['maxplaytime'] = int(row[3])
                game_info['minage'] = int(row[4])
                game_info['average'] = float(row[5])
                game_info['avgweight'] = float(row[6])
                
                boardgames[row[0]] =  game_info
                #Key is the name of the game, value is game_info dict
    return boardgames

    
def recommend_game(dictionary, boardgame):
    '''
    Function:
        Recommends a boardgame based on your inputted boardgame
    Parameter: 
        dictionary with all the boardgames, desired boardgame name (string)
    Return: 
        List of each game info variable ordered from closest to the inputted
        board game's to the farthest away
    '''
    
    inputted_gameinfo = list(dictionary[boardgame].values())
    #This turns all the info about the desired board game into a list
    #ie. a list full of info about the game's minplaytime, minage, etc.
    
    dictionary.pop(boardgame)
    #Get rid of the inputted boardgame because we don't want to
    #compare it to itself
    
    closest_match = [10000, 'none']
    #Instantiates a placeholder game that will eventually become the game
    #most similar to the inputted boardgame
    
    for key, value in dictionary.items():
        
        other_gameinfo = list(value.values())
        similarness = math.sqrt(sum(((x - y)**2) 
                               for x, y in zip(inputted_gameinfo, other_gameinfo)))
        #This is just the formula for calculating Euclidean distance
    
        if similarness <= closest_match[0]:
            #Narrows down Euclidean distance between games until it arrives at
            #the smallest distance and therefore most similar game
            closest_match[0] = similarness
            closest_match[1] = key

    print("Here's our recommendation! \n" + closest_match[1])
    print('\nThis is how similar our recommendation is to ' + boardgame + ': ' 
          + str(closest_match[0]))
    return closest_match
        

def chart_ratings(boardgames_dict):
    '''
    Function:
        Create a barchart 
    Parameter:
        dictionary with all the ratings and their respective # of occurrences
    Return: 
        a barchart with ratings on x-axis and the # of occurrences on y-axis
    '''
    rating_levels = [i for i in range(11)]
    #These will be the x-ticks for the barchart
    ratings = [round((value['average'])) for value in boardgames_dict.values()]
    #Retrieve and round average ratings to nearest integer
    
    #Plot histogram with ratings on x-axis and # of times they appear
    #on the y-axis
    plt.hist(ratings, rating_levels, color = 'orchid')
    plt.title("Boardgame Ratings")
    plt.xlabel("Average Rating")
    plt.ylabel("# of Boardgames")
    plt.xticks(rating_levels)
    #Make x-axis ticks #'s 1-9
    
    
def plot_ratings_weight(boardgames_dict):
    '''
    Function:
        Creates a scatterplot
    Parameter:
        dictionary with all the boardgames
    Return: 
        A scatterplot with game weight on x-axis and rating on y-axis
    '''
    
    game_weights = [value['avgweight'] for value in boardgames_dict.values()]
    
    ratings = [value['average'] for value in boardgames_dict.values()]
    
    #List comprehension: created a list full of all boardgame weight values and 
    #a lsit of all boardgame rating values. Took only the values where avg weight 
    #was not 0 and rating was not 0 because I feel as those simply lacked info.
    
    plt.scatter(game_weights, ratings, color = "lightblue")
    plt.xlabel("Game Weight (lb))")
    plt.ylabel("Average User Rating")
    plt.title("Correlation between Boardgame Weight and Avg. User Rating")

                      
if __name__ == "__main__":
    
    #Question 1 (Read in csv file, get rid of games that don't support solo mode)
    boardgames = csv_to_dict(FILENAME)
    
    #Question 2 (Make a recommendation for Mage Knight Board Game)
    recommendation = recommend_game(boardgames, MAGE)
    
    
    #Question 3 (Visualizations: Plot # of games in each rating, plot relationship
    #between avg. user rating and boardgame weight)
    chart_ratings(boardgames)
    plt.savefig('Average User Ratings for Boardgames')
    plt.show()
    plot_ratings_weight(boardgames)
    plt.savefig('Ratings&Weight')
    plt.show()
    
    '''
    There does seem to be a correlation between average game weight and 
    average user rating which isn't surprising, the heavier it is,
    the more complex, comprehensive, and thoughtful the game usually is.
    '''
    
    #Question 4
    
    '''
    I would suggest trying to break into the market with a more complex, thought
    out, intensive, and therefore expensive and heavier game. The reason why 
    I think this is because markets nowadays are so oversaturated with cheap, 
    mass-produced products and for present-day entrepreneurs, I believe that 
    they experience more success when targeting more niche, untapped markets. 
    It would be nearly impossible to profit after breaking into, let's say, 
    the deck of cards industry. Bicycle and tons of other companies would devour you. 
    It would be much easier, however, to create an entirely original game with 
    tons of intricacies, pieces, and unique game mechanics, and try and target 
    your game to a smaller target market who is able to afford its high prices. 
    And as we see, if you do decide to create a heavier boardgame, the ratings 
    seem to trend upwards with it. For these reasons, I would suggest creating 
    a game in the 4-5 lb range. After you build up your reputation and your product 
    has been happily received by the market, then you can go after the bigger companies.
    '''