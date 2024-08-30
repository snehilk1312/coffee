import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

roaster = 'bloom_coffee_roasters'
# Base URL for coffee products
base_url = "https://bloomcoffeeroasters.in/collections/coffee?page="
total_page = 2
# Prepare the CSV file
csv_file = 'coffee_bloomcoffeeroasters.csv'
csv_columns = ['name', 'price', 'link', 'tasting_notes', 'elevation', 'varietal', 'planters', 'processing', 'roast', 'description']

# Function to get additional product details from the product page
def get_product_details(product_url):
    product_response = requests.get(product_url)
    product_soup = BeautifulSoup(product_response.content.lower(), 'html.parser')
    
    details = {
        'tasting notes': None,
        'elevation': None,
        'varietal': None,
        'variety': None,
        'planters': None,
        'planter': None,
        'producer': None,
        'producers': None,
        'processing': None,
        'roast': None
    }
    
    # Extracting product details from the product page
    details_section = product_soup.find('div', class_='product-single__description')
    if details_section:
        details_text = details_section.text
        for key in details.keys():
            # if key.replace('_', ' ').capitalize() + ':' in details_text:
            #     details[key] = details_text.split(key.replace('_', ' ').capitalize() + ':')[1].split('\n')[0].strip()
            if key.replace('_', ' ') + ':' in details_text:
                details[key] = details_text.split(key.replace('_', ' ') + ':')[1].split('\n')[0].strip()  
        details['description'] = details_section.text

    return details

# Write to CSV file
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

    for page in range(1, total_page+1):  # Iterating through pages 1, 2, and 3
        url = base_url + str(page)
        response = requests.get(url)
        html_content = response.content.lower()

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all the products
        products = soup.find_all('div', class_=['grid-product'])

        for product in products:
            name_tag = product.find('p', class_='grid-product__title')
            name = name_tag.text.strip() if name_tag else None

            price_tag = product.find('span', class_='money')
            price = price_tag.text.strip() if price_tag else None

            link_tag = product.find('a', class_='grid-product__image-link')
            link = 'https://bloomcoffeeroasters.in' + link_tag['href'] if link_tag else None

            product_details = get_product_details(link) if link else {}
            
            writer.writerow({
                'name': name,
                'price': price,
                'link': link,
                'tasting_notes': product_details.get('tasting notes'),
                'elevation': product_details.get('elevation'),
                'varietal': product_details.get('varietal') if product_details.get('varietal') else product_details.get('variety'),
                'planters': product_details.get('planter') if product_details.get('planter') else product_details.get('planters') if product_details.get('planters') else product_details.get('producers') if product_details.get('producers') else product_details.get('producer'),               
                'processing': product_details.get('processing'),
                'roast': product_details.get('roast'),
                'description': product_details.get('description')
            })

print(f"Data has been written to {csv_file}")

# putting it into db

conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
df = pd.read_csv(csv_file)
df['scraped_at'] = datetime.now()
df.to_sql(name = roaster , con=conn, index=False, if_exists='append',schema='raw_scraped')