import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv
import re

def extract_properties(text):
    # Convert text to lowercase
    text = text.lower()

    properties = {
        'estate': None,
        'location': None,
        'brix': None,
        'block': None,
        'varietal': None,
        'processing': None,
        'tasting_notes': None,
        'elevation': None,
        'roast_level': None,
    }
    
    # Estate
    estate_match = re.search(r'estate\s*name\s*=\s*(.+?)\. location:', text)
    if not estate_match:
        estate_match = re.search(r'from our farm (.+?) estate', text)
    if estate_match:
        properties['estate'] = estate_match.group(1).strip()

    # Location
    location_match = re.search(r'location\s*:\s*(.+)', text)
    if location_match:
        properties['location'] = location_match.group(1).strip()

    # BRIX
    brix_match = re.search(r'brix\s*:\s*([\d\.]+)', text)
    if brix_match:
        properties['brix'] = brix_match.group(1).strip()

    # Block
    block_match = re.search(r'block\s*:\s*(.+?)\.', text)
    if block_match:
        properties['block'] = block_match.group(1).strip()

    # Varietal
    varietal_match = re.search(r'varietal\s*:\s*(.+?)\.', text)
    if varietal_match:
        properties['varietal'] = varietal_match.group(1).strip()

    # Processing
    processing_match = re.search(r'processing\s*:\s*(.+?)\.', text)
    if processing_match:
        properties['processing'] = processing_match.group(1).strip()

    # Tasting Notes
    tasting_notes_match = re.search(r'tasting notes\s*:\s*(.+)', text)
    if tasting_notes_match:
        properties['tasting_notes'] = tasting_notes_match.group(1).strip()

    # Elevation
    elevation_match = re.search(r'elevation\s*:\s*(.+?)(?:m|meters?)', text)
    if elevation_match:
        properties['elevation'] = elevation_match.group(1).strip()

    # Roast Level
    roast_level_match = re.search(r'roast\s*level\s*:\s*(.+)', text)
    if roast_level_match:
        properties['roast_level'] = roast_level_match.group(1).strip()

    return properties

load_dotenv()

roaster = 'rossette'

# Base URL for the coffee collection
base_url = "https://www.fraction9coffee.com"
collection_url = f"{base_url}/collections/coffee"
response = requests.get(collection_url)
content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# List to store coffee details
coffee_details = []
count=0
# Find all coffee product links
for product in soup.find_all('div',class_='product-card__details'):
    link_tag = product.find('a', href=True,title=True)

    if link_tag:
        name = link_tag['title']
        product_url = base_url + link_tag['href']  # Construct the full URL

        # Fetch the individual product page to extract additional details
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.content, 'html.parser')

        # Extract relevant product properties
        coffee_properties = {
            'name': name,
            'url': product_url
        }

        prop_tag = product_soup.find('div', class_='product-single__box__block--description')
        description = prop_tag.get_text(separator=" ", strip=True)
        description = description.replace('💥',' ')

        coffee_properties.update(extract_properties(description))

        # coffee_properties["price"] = product_soup.find('span', class_='price-item').text.strip()
        # coffee_properties["description"] = product_soup.find('p', {"x-ref": "para"})['data-desc']

        # Append the coffee details to the list
        # coffee_details.append(coffee_properties)
        print(coffee_properties)