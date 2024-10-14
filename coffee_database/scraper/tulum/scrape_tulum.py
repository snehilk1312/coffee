import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

roaster = 'tulum'

# Fetch homepage content
url = "https://www.tulum.coffee/collections/roasted-coffees"
response = requests.get(url)
html_content = response.content

# Parse the homepage content
soup = BeautifulSoup(html_content, 'html.parser')
base_url = 'https://www.tulum.coffee'

# Find the product grid containing the coffee names and links
product_grid = soup.find('ul', {'id': 'product-grid'})

# Initialize a dictionary to store the coffee names, links, and prices
coffee_details = []

# Loop through each list item (coffee entry)
for item in product_grid.find_all('li', class_='grid__item'):
    # Find the coffee name (inside the <h3> tag with class 'card__heading')
    name_tag = item.find('h3', class_='card__heading')
    if name_tag:
        name = name_tag.text.strip()

        # Find the link (inside the <a> tag)
        link_tag = name_tag.find('a')
        link = f"{base_url}{link_tag['href']}" if link_tag and 'href' in link_tag.attrs else None

        # Find the price (inside the 'price__regular' class)
        price_tag = item.find('span', class_='price-item--regular')
        price = price_tag.text.strip() if price_tag else None

        coffee_properties = {
            'name': name,
            'url': link,
            'price': price,
            'flavour notes': None,
            'location': None,
            'altitude': None,
            'varietal': None,
            'roast level': None,
            'process': None,
            'description': None,
            'suggested equipment': None,
            'planters name': None,
            'farm name': None
        }

        # Parse the HTML content
        item_response = requests.get(link).content.lower()
        item_soup = BeautifulSoup(item_response, 'html.parser')

        # Scrape the product description
        description_tag = item_soup.find('div', class_='product__description rte quick-add-hidden')
        if description_tag:
            description = description_tag.get_text(separator=' ', strip=True)
            coffee_properties['description'] = description

        # Scrape specific properties from the table
        property_rows = description_tag.find_all('tr') if description_tag else []

        for row in property_rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                property_name = cells[0].get_text(strip=True)
                property_value = cells[1].get_text(strip=True)
                coffee_properties[property_name] = property_value

        coffee_properties['tasting_notes'] = coffee_properties.pop('flavour notes', coffee_properties.get('flavor notes'))
        coffee_properties['roast_level'] = coffee_properties.pop('roast level', coffee_properties.get('roast level'))
        coffee_properties['estate'] = coffee_properties.pop('farm name', coffee_properties.get('farm name'))
        coffee_properties['producers'] = coffee_properties.pop('planters name', coffee_properties.get('planters name'))
        coffee_properties['suggested_equipment'] = coffee_properties.pop('suggested equipment', coffee_properties.get('suggested equipment'))
        coffee_details.append(coffee_properties)


# Define the CSV file headers
headers = ["name","url","price",'location','altitude','varietal','process',"description",'tasting_notes','roast_level','estate','producers','suggested_equipment']

# Write the combined data to a CSV file
csv_filename = f'{roaster}.csv'
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