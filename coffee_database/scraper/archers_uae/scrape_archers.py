import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv
import re

load_dotenv()

roaster = 'archers_uae'

# get exchange rate aed to inr
response_er = requests.get("https://api.exchangerate-api.com/v4/latest/AED")  
exchange_rate = response_er.json()['rates']['INR']


# Fetch homepage content
url = "https://archerscoffee.com/collections/coffee"
response = requests.get(url)
html_content = response.content

# Parse the homepage content
soup = BeautifulSoup(html_content, 'html.parser')
base_url = 'https://archerscoffee.com'

# Find the product grid containing the coffee names and links
product_grid = soup.find_all('div', class_='product__grid__info')

# Initialize a dictionary to store the coffee names, links, and prices
coffee_details = []

for i  in product_grid:
    name = i.find('p', class_='product__grid__title').get_text(strip=True)
    taste = i.find('div', class_='taste').get_text(strip=True)
    price = round(float(i.find('lomoney').get_text(strip=True))*exchange_rate,2)
    product_url = base_url + i.find('a', {'href': True})['href']

    coffee_properties = {
            'name': name,
            'url': product_url,
            'tasting_notes': taste,
            'price': price
        }

    # print(coffee_properties)

    product_response = requests.get(product_url)
    product_soup = BeautifulSoup(product_response.content, 'html.parser')

    description = product_soup.find('div', class_='product-accordion').get_text(separator=" ").lower()

    info_set1 = {}
    key_set1 = ["producer", "farm", "location", "variety", "process", "altitude"]
    pattern = r"(?:" + "|".join(re.escape(key) for key in key_set1) + r")\s*:\s*.*?(?=(?:\s+" + r"|".join(re.escape(key) for key in key_set1) + r")\s*:|$)"

    # Find all matches
    matches = re.findall(pattern, description)

    for match in matches:
        key, value = map(str.strip, match.split(":", 1))
        info_set1[key] = value


        
    # Dictionary to store the extracted information
    print(product_url)
    print(info_set1)

    # print(description)

    print('*'*200)
