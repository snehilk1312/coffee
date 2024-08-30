import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os,re
from dotenv import load_dotenv

load_dotenv()

roaster = 'blue_tokai'
csv_file = 'coffee_blue_tokai.csv'
def fetch_coffee_data(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    coffee_blocks = soup.find_all('a', class_='grid-product__link')
    coffee_list = []
    for block in coffee_blocks:
        name_tag = block.find('div', class_='grid-product__title')
        name = name_tag.text.strip() if name_tag else 'No name found'

        flavor_tag = block.find_next('div', class_='customvariants')
        flavor = flavor_tag.text.strip() if flavor_tag else 'No flavor description found'

        link = block.get('href')
        full_link = f'https://bluetokaicoffee.com{link}' if link else 'No link found'

        additional_details = fetch_additional_details(full_link)

        coffee_details = {
            'name': name,
            'flavor': flavor,
            'link': full_link,
        }
        coffee_details.update(additional_details)
        coffee_list.append(coffee_details)
    
    return coffee_list

def fetch_additional_details(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    additional_details = {
        'sweetness': 'Not available',
        'body': 'Not available',
        'acidity': 'Not available',
        'bitterness': 'Not available',
        'roast': 'Not available',
        'have_it': 'Not available',
        'altitude': 'Not available',
        'processing': 'Not available',
        'location': 'Not available',
        'variety': 'Not available',
        'blue_tokai_class': 'Not available',
        'description': 'Not available',
        'price': 'Not available'
    }
    
    compare_fields = soup.find_all('div', class_='compare-items-coloum')
    details_fields = soup.find_all('div', class_='details-items-coloum')
    
    def extract_details(fields):
        for field in fields:
            p_tag = field.find('p')
            if p_tag and p_tag.find('b'):
                key = p_tag.find('b').get_text(strip=True).lower().replace(' ', '_')
                value = p_tag.get_text(strip=True).replace(p_tag.find('b').get_text(strip=True), '').strip()
                additional_details[key] = value
    
    extract_details(compare_fields)
    extract_details(details_fields)
    
    # Extract blue_tokai_class
    blue_tokai_class_tag = soup.find('h4', class_='cd-bg-text')
    if blue_tokai_class_tag:
        additional_details['blue_tokai_class'] = blue_tokai_class_tag.get_text(strip=True)
    
    # Extract description
    description_tag = soup.find('div', class_='cdfulltext')
    if description_tag:
        additional_details['description'] = description_tag.get_text(strip=True)

    # Extract price
    price_tag = soup.find('span',class_='product__price')
    if price_tag:
        additional_details['price'] = price_tag.get_text(strip=True)

    return additional_details

# Base URL for the collection
base_url = 'https://bluetokaicoffee.com/collections/roasted-and-ground-coffee-beans?page='

all_coffee_list = []
num_pages = 2

for page in range(1, num_pages + 1):
    url = base_url + str(page)
    print(f"Fetching page {page}...")
    coffee_list = fetch_coffee_data(url)
    all_coffee_list.extend(coffee_list)

# Determine all unique fieldnames
fieldnames = set()
for coffee in all_coffee_list:
    fieldnames.update(coffee.keys())
fieldnames = list(fieldnames)

# Print extracted coffee details
for coffee in all_coffee_list:
    # print(f"Name: {coffee['name']}, Flavor: {coffee['flavor']}, Link: {coffee['link']}")
    for key, value in coffee.items():
        print(f"{key.capitalize()}: {value}")
    print('-'*100)

# Save to a CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for coffee in all_coffee_list:
        writer.writerow(coffee)

# arrange columns

df = pd.read_csv(csv_file)
all_columns = [
        'name',
        'price',
        'roast',
        'have_it',
        'sweetness',
        'body',
        'processing',
        'altitude',
        'acidity',
        'location',
        'bitterness',
        'varietal',
        'flavor',
        'variety',
        'tasting_notes',
        'description',
        'blue_tokai_class',
        'link'
]

# taking care of extra or less columns
columns_found  = [i for i in df.columns.tolist() if i in all_columns]
df = df[columns_found]
columns_missing = [i for i in all_columns if i not in df.columns.tolist()]
df[columns_missing] = None
df = df[all_columns]

df.to_csv(csv_file,index=False)

print("Coffee information saved to coffee_blue_tokai.csv")

# putting it into db

conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
df = pd.read_csv(csv_file)
df['scraped_at'] = datetime.now()
df.to_sql(name = roaster , con=conn, index=False, if_exists='append',schema='raw_scraped')