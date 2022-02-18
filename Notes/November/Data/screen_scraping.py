"""
Daniel Xu
November 17th, 2021
In Class Notes: Datascraping
Professor Raichlin
"""

import requests
from bs4 import BeautifulSoup


URL = 'https://nssdc.gsfc.nasa.gov/planetary/factsheet/'

response = requests.get(URL)
print(response)

# webpage contents
content = response.content
