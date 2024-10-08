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

roaster = 'fraction9'

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
        # print(description)

        # coffee_properties.update(extract_properties(description))

        try:    
            coffee_properties["price"] = product_soup.find('span', class_='price__number').text.strip()
        except:
            coffee_properties["price"] = None

        coffee_properties["description"] = name +' ' + description
        coffee_properties["description"] = coffee_properties["description"].lower()

        if 'kalyancool' in coffee_properties["description"]:
            coffee_properties["description"] = coffee_properties["description"].replace('kalyancool', 'estate : kalyancool estate')

        # Append the coffee details to the list
        coffee_details.append(coffee_properties)
        # print(coffee_properties)
        # print('*'*100)


# Define the CSV file headers
headers = ["name", "url", "price","description"]

# Write the combined data to a CSV file
csv_filename = 'fraction9.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for row in coffee_details:
        writer.writerow(row)

print(f"Data saved to {csv_filename}")


# putting it into db

conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
df = pd.read_csv(csv_filename)
df['scraped_at'] = datetime.now()
df.to_sql(name = roaster , con=conn, index=False, if_exists='append',schema='raw_scraped')