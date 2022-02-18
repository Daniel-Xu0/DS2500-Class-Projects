# -*- coding: utf-8 -*-
"""
@author: John Rachlin
@date  : September 13, 2021
@file  : cherry.py

Analysis of the full-flowering day-of-year for cherry blossums 
in Kyoto Japan.

Why is this significant?   Scientists are interested in understanding
periodic biological phenomena (flowering, breeding, migration) 
especially as it relates to climatic conditions.  (The scientific
study of these types of phenomena is known as PHENOLOGY.)

Data source: https://www.ncei.noaa.gov/pub/data/paleo/historical/phenology/japan/LatestVersion/KyotoFullFlower7.xls

Data for 2020 and 2021 added to data set.

2020: March 30 - based on Japan Meterological Corporation (JMC) 2020 forecast. 
2021: March 26 - based on reported actual (Osaka University)

"""



import csv
import matplotlib.pyplot as plt

def read_flowering_data(filename):
    """ Read cherry blossum full-flowering day-of-year data.
    Return a dictionary mapping year to day-of-year (of full blossums) """
    
    data = {}
    
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            year = int(row[0])
            if row[1] != '':
                doy = int(row[1])
                data[year] = doy 
    return data



def blossum_date_moving_average(bldata, window_size=50):
    """ Compute a moving average using a specified window size. """

    moving_average = {}

    # For each data point, acccumulate all values
    # the window span of that year
    for year in bldata:
        for window_year in range(year - window_size//2, year + window_size//2):
            if window_year in bldata:
                moving_average[window_year] = moving_average.get(window_year,[]) + [bldata[year]]

    # Convert each aggregate (window values) to an average
    for year in moving_average:
        moving_average[year] = sum(moving_average[year]) / len(moving_average[year])

    return moving_average


def plot_blossum_day_history(bldata, mavgdata):
    """ Plot the day-of-year full blossuming by year
    for all available years """
    
    years = bldata.keys()
    days = bldata.values()
    
    moving_averages = mavgdata.values()
    
    plt.figure(figsize=(10,6), dpi=100)
    plt.title("Cherry Blossom full blossom date (Kyoto, Japan)")
    plt.xlabel("Year")
    plt.ylabel("Date")

    plt.scatter(years, days, marker='.', color='#FF66B2', label='Full blossom date') # The color of cherry blossums!
    plt.plot(years, moving_averages, color='b', label='30 year moving avg')

    plt.yticks([80,90,100,110,120], ['Mar 21', 'Mar 31', 'Apr 10', 'Apr 20', 'Apr 30'])

    
    # Highlight 2021 (Record)
    plt.text(1900, 84.5, '2021 --->')
    
    # Outliers are interesting!
    # There was a global temperature reduction at that time.
    # See global_temps.png
    
    plt.text(1333,124, '1323 (May 4th)')
    plt.text(1416, 86, '1409') # Until 2021, this was the previous record year
    
    # Annotate figure with "The little ice-age" - a period of cooling
    # occurring between 1400-1800, though, according to wikipedia,
    # some experts prefer the alternative timespan of 1300-1850
    
    plt.text(1300,84, '<- - - - - -------- The "Little Ice Age" ---------- - ->')

    # Include a legend
    plt.legend(facecolor='lightgrey', edgecolor='black')
    plt.grid()
    plt.show()
    
    



def main():
    
    # Read the data into a dictionary (year -> doy)
    blossum_day_data = read_flowering_data('cherry.csv')
    
 
    # Compute blossum day 50-year moving averages
    moving_average = blossum_date_moving_average(blossum_day_data, 30)

    
    # Visualize full-blossum day-of-year (Kyoto, Japan)
    plot_blossum_day_history(blossum_day_data, moving_average)
        
    
    
if __name__ == '__main__':
    main()
