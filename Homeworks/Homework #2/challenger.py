"""
Daniel Xu
DS2500 - HW #2: The Challenger Accident
Prof. Park and Raichlin
September 30th, 2021
"""

import numpy as np
import pandas as pd
import math
import seaborn as sns
import matplotlib.pyplot as plt

#CSV filenames
STATIONS = 'stations.csv'
TEMPS_1986 = 'temp_1986.csv'

#Create column names for stations and temps dataframes
station_columns = ['station_ID', 'wban_ID', 'latitude', 'longitude']
temp_columns = ['station_ID', 'wban_ID', 'month', 'day', 'temp']

#Set Cape Canaveral's (C.C) geographic location to constants
CAPE_LAT = 28.396837
CAPE_LONG = -80.605659

'''
Kept on getting this error, even after using .loc to index DF columns:
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead
#https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#r
#eturning-a-view-versus-a-copy. 
The line below suppresses the error message.
'''
pd.options.mode.chained_assignment = None

def read_csvfiles(filename1, filename2):
    '''
    Function: Read csvfiles into a dataframe
    Parameters: two different csv files
    Return: Two separate dataframes
    '''
    
    file1 = pd.read_csv(filename1, header = None)
    #Add in station column names to dataframe
    file1.columns = station_columns
    
    file2 = pd.read_csv(filename2, header = None)
    #Add in temp column names to dataframe
    file2.columns = temp_columns
    
    return file1, file2

def clean_stations(stations):
    '''
    Function: Get rid of null, missing, or inalid values in the stations dataframe
    Parameters: a dataframe
    Return: A cleaned up dataframe
    '''
    
    #Get rid of the wban_ID columns since we don't need it
    stations.drop(['wban_ID'], axis = 1, inplace = True)
    
    #Get rid of the rows with any null values, these would be the stations
    #without a longitude/latitude 
    stations.dropna(inplace = True)
    
    #Get rid of any duplicates
    stations.drop_duplicates(inplace = True)
    
    #Get rid of the rows that have invalid values, the stations with a latitude
    #of 0.00 and a longitude of 00.000
    updated_stations = stations[stations['latitude'] != 0]
    return updated_stations
    
def clean_temps(temps):
    '''
    Function: Get rid of null, missing, or inalid values in the stations dataframe
    Parameters: a dataframe
    Return: A cleaned up dataframe
    '''
    
    #Once again getting rid of wban_ID columns
    temps.drop(['wban_ID'], axis = 1, inplace = True)
    
    #Get rid of all the rows that have an empty temperature value
    temps.dropna(inplace = True)
    
    return temps

def combine_dataframes(df_1, df_2):
    '''
    Function: Combine useful columns between the two dataframes into one dataframe
    Parameters: two dataframes
    Return: A dataframe with only the columns that we need
    '''
    #Super useful and interesting pandas function which merges two dataframes,
    #stations and temps, and combines them based on the intersection of their 
    #station ID's
    combined_df = pd.merge(df_1, df_2, on = 'station_ID', how = 'inner')
    
    #Get rid of all the  data that wasn't recorded in January since all we care
    #about is what happened to the Challenger in January.
    jan_df = combined_df[combined_df['month'] == 1]
    #We also need February data; however, for the temperature visualization
    feb_df = combined_df[combined_df['month'] == 2]
    
    #Change the indices of the dataframe to just be the row number
    jan_df.reset_index(inplace = True)
    feb_df.reset_index(inplace = True)
    
    return jan_df, feb_df

def calc_haversine(dataframe):
    '''
    Function: calculate haversine distance between C.C and weather stations
    Parameters: a single dataframe
    Return: a new dataframe with only stations that are within 100km of 
            C.C
    '''
    
    #Haversine Distance Formula Acquired from here: 
    #https://stackoverflow.com/questions/4913349/haversine-formula-in-python
    #-bearing-and-distance-between-two-gps-points
    
    #Create a new column which will contain the distance from each location
    #to C.C
    dataframe['distance_to_cape'] = np.nan
    
    for index, row in dataframe.iterrows():
        # distance between latitudes and longitudes
        distance_Lat = math.radians((row['latitude'] - CAPE_LAT))
        distance_Long = math.radians((row['longitude'] - CAPE_LONG))
    
        #convert to radians
        radian_station_Lat = math.radians(row['latitude'])
        radian_cape_Lat = math.radians(CAPE_LAT)
    
        #Apply formulae
        a = (pow(math.sin(distance_Lat / 2), 2) + pow(math.sin(distance_Long / 2), 2) 
              * math.cos(radian_station_Lat) * math.cos(radian_cape_Lat))
        
        radius = 6371
        c = 2 * math.asin(math.sqrt(a))
        distance = radius * c
        
        #If the distance from the location to C.C is 100km or less,
        #we add it to the dataframe
        if distance <= 100:
            dataframe.at[index, 'distance_to_cape'] = distance
    
    dataframe.dropna(inplace = True)
    return dataframe
    

def inverse_distance(dataframe):
    '''
    Function: Calculate the weighted distance between C.C and each
              location in the dataframe
    Parameters: A dataframe
    Return: Dataframe with new column of each location's weighted distance
    '''
    #p-value for inverted distance calculations
    p = 1
    
    #Create two columns in the dataframe which are the weight factor and 
    #weighted temperature at each location 
    dataframe['inv_distance'] = 1 / (dataframe['distance_to_cape'] ** p)
    dataframe['weighted_temp'] = dataframe['temp'] * dataframe['inv_distance']
    
    #Finally calculate 
    daily_temps = (dataframe.groupby('day').weighted_temp.sum() / 
                  dataframe.groupby('day').inv_distance.sum())
    
    #Change daily_temps series into a Dataframe with column names
    daily_temps = pd.DataFrame({'Day': daily_temps.index, 
                                'Temperature': daily_temps.values})
    return daily_temps


def plot_temps(daily_temps):
    '''
    Function: Plot the temperatures in C.C for January
    Parameters: a series of temperature data
    Return: A plot depicting the change in temperature in C.C January
    '''
    
    #Create a regular lineplot for C.C's January temps
    cape_temps = sns.relplot(data = daily_temps, x= 'Day', y = 'Temperature', 
                             kind="line")
    
    #Set title, y-label, and x-label
    cape_temps.set(xlabel = 'Day of the Month', ylabel = 'Daily Temperature (°F)',
                   title = "Cape Canaveral's Daily Temperatures in January")


#This is now the start of Problem #2: Mapping the Weather Throughout the US
def map_locations(combined_df, month, day, date):
    '''
    Function: Create colored weather map of specified date using numpy array
    Parameters: dataframe with combined geographical and temperature data, 
                a month (int), and a day (int)
    Return: A plot that shows how the temperature looked like around the East
            coast of the United States
    '''
    
    '''The 100x150 array represents longitudes from -125 to -65 degrees
    #So cape canaveral is (-80.605659 - (-125)) / (-65 - (-125)) = 73.99%
    #in other words, the y index for C.C is at int(.07399 x 150) = 110
    #Do the exact same thing for the X- coordinate'''
    
    #Leave only the stations that have a latitude of [25,50] and a longitude
    #of [-125, -65]
    nearby_stations = combined_df[(combined_df.latitude > 25) & 
                              (combined_df.latitude < 50) & 
                              (combined_df.longitude > -125) &
                              (combined_df.longitude < -65)]
    
    #Find the data for just the date specified
    spec_date = nearby_stations[(nearby_stations['month'] == month) & 
                                    (nearby_stations['day'] == day)]
    
    #Calculate the x-pos and y-pos on our numpy array that each stations will map to
    spec_date['x-coord'] = round(((spec_date.loc[:, 'latitude'] - 25) / 50) * 100)
    spec_date['y-coord'] = round(((spec_date.loc[:, 'longitude'] + 125) / 60) * 150)
    
    #Drop a few columns to make the df more readable
    spec_date.drop(['station_ID', 'latitude', 'longitude'], axis = 1, inplace = True)
    
    spec_date.reset_index(inplace = True)
    
    
    ''''What's interesting here is that the datatype 
    #directly influences the overall image. If the datatype was int8 my 
    #plot would look like a broken TV. If the datatype was int16, my jan_1 data
    #would look amazing but the feb_1 data would look like a Leprachaun's vomit.
    #I can't seem to wrap my head around why the datatype has such a drastic 
    #effect on the image'''
    
    #Create an empty array that'll store the RGB values of each station's 
    #respective temperature. 
    map_temps = np.empty((100, 150, 3), dtype = np.int32)
    
    #https://www.webucator.com/article/python-color-constants-module/
    #Here's the article I used to find out all the RGB constants for the 
    #colors on my map
    
    for i in spec_date.index:
        #Iterate over dataframe to instantiate each x-coord, y-coord, and 
        #respective temp
        x_coord = int(spec_date.loc[i, 'x-coord'])
        y_coord = int(spec_date.loc[i, 'y-coord'])
        temp = spec_date.loc[i, 'temp']
        if temp <= 10:
            #Aqua
            map_color = [0, 255, 255]
        elif temp > 10 and temp <= 20:
            #BLue
            map_color = [0, 0, 255]
        elif temp > 20 and temp <= 30:
            #Dark Green
            map_color = [0, 70, 0]
        elif temp >30 and temp <= 40:
            #Lime Green 
            map_color = [90, 215, 90]
        elif temp > 40 and temp <= 50:
            #Light Green
            map_color = [0, 255, 0]
        elif temp > 50 and temp <= 60:
            #Yellow
            map_color = [255, 235, 0]
        elif temp > 60 and temp <= 70:
            #Cadmium Orange
            map_color = [255, 97, 0]
        else:
            #Red Orange
            map_color = [250, 69, 0]
        
        #Put the temperature's RGB value into the numpy array at its 
        #corresponding coordinates
        map_temps[x_coord][y_coord] = map_color
    
    plt.figure(figsize = (7, 7))  
    plt.imshow(map_temps, interpolation = 'none')
    plt.ylim(0, 55)
    plt.title("Average Temeprature Around the US on " + date)

    return map_temps

def main():
    '''
    Function: Execute and compile other functions into one single function
    Parameters: None
    Return: A plot of Cape Canaveral's daily temps in January
    '''
    #Problem 1: Finding the temp of Cape Canaveral
    #Read in csv files into dataframes
    stations, temps = read_csvfiles(STATIONS, TEMPS_1986)
    
    #Clean the dataframes
    cleaned_stations = clean_stations(stations)

    cleaned_temps = clean_temps(temps)

    #Combine the dataframes, intersect by 'station_ID' columm
    jan_df, feb_df = combine_dataframes(cleaned_stations, cleaned_temps)
    

    #Problem 2: Visualizing Temp in the US
    jan_28 = map_locations(jan_df, 1, 28, "January 28th")
    feb_1 = map_locations(feb_df, 2, 1, "February 1st")
    

    # #Create a new column which has only the data for stations within 100km
    # #of Cape Canaveral
    # closest_stations_df = calc_haversine(jan_df)

    # #Calculate temperature of C.C from temperatures at other stations
    # january_temps = inverse_distance(closest_stations_df)
    
    # #Plot C.C temperatures throughout January
    # plot_temps(january_temps)
    


if __name__ == "__main__":
    main()
    
    