import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

roaster = 'koffie_genetics'

# Fetch webpage content
url = "https://genetics.coffee/collections/all"
response = requests.get(url)
html_content = response.content.lower()

# Parse the webpage content
soup = BeautifulSoup(html_content, 'html.parser')

# Base URL for links
base_url = "https://genetics.coffee"

# Extract product information
products = []
for product in soup.find_all('li', class_='grid__item'):
    name = product.find('h3', class_='card__heading').get_text(separator=" ", strip=True)
    availability = product.find('div', class_='card__badge').get_text(separator=" ", strip=True)
    price = product.find('span', class_='price-item--regular').get_text(separator=" ", strip=True)
    link = base_url + product.find('a', class_='full-unstyled-link')['href']
    
    products.append([name, availability, price, link])

# Define a function to scrape properties from individual product pages
def scrape_properties(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text.lower(), 'html.parser')
    
    # Initialize a dictionary to store the properties
    properties_temp = {
        "varietal": "",
        "roast": "",
        "sca cup score": "",
        "process": "",
        "origin": "",
        "altitude":"",
        "producer":"",
        "specie":"",
        "tasting notes":"",
        "description": "",
        "elevation":"",
        "region":"",
        "impressions":"",
        "impression":"",
        "tastes like":"",
        "type":""
    }
    
    properties={}
    details_text = soup.find('div', class_='product__description').text
    details_text = details_text.replace('elevation','altitude')
    details_text = details_text.replace('region','origin')
    details_text = details_text.replace('impressions','tasting notes')
    details_text = details_text.replace('impression','tasting notes')
    details_text = details_text.replace('tastes like','tasting notes')
    details_text = details_text.replace('type','specie')

    for title in properties_temp.keys():
        if len(details_text.split(title))>1:
            properties[title] = details_text.split(title)[1].strip().strip(':').strip().strip('|').strip()
            for title_inner in properties_temp.keys():
                if len(properties[title].split(title_inner))>1:
                    properties[title] = properties[title].split(title_inner)[0]

    properties['description'] = details_text
        
    return properties

# Combine product information with detailed properties
detailed_products = []
for product in products:
    name, availability, price, link = product
    properties = scrape_properties(link)
    detailed_product = {
        "name": name,
        "availability": availability,
        "price": price,
        "link": link,
        **properties
    }
    detailed_products.append(detailed_product)

# Define the CSV file headers
headers = ["name", "availability", "price", "link", "varietal", "roast", "sca cup score", "process", "origin","altitude","producer","specie","tasting notes","description"]

# Write the combined data to a CSV file
csv_filename = 'koffie_genetics_detailed_products.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for row in detailed_products:
        writer.writerow(row)

print(f"Data saved to {csv_filename}")


# putting it into db

conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
df = pd.read_csv(csv_filename)
df['scraped_at'] = datetime.now()
df.to_sql(name = roaster , con=conn, index=False, if_exists='append',schema='raw_scraped')