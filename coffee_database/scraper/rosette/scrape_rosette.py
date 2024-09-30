import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

roaster = 'rossette'

# Base URL for the coffee collection
base_url = "https://rossettecoffee.com"
collection_url = f"{base_url}/collections/coffee"
response = requests.get(collection_url)
content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# List to store coffee details
coffee_details = []

# Find all coffee product links
for product in soup.find_all('a', href=True):
    # Check if the product contains the necessary structure
    h3_tag = product.find('h3', class_='font-semibold')
    if h3_tag:
        name = h3_tag.text.strip()  # Extract the name
        product_url = base_url + product['href']  # Construct the full URL

        # Fetch the individual product page to extract additional details
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.content, 'html.parser')

        # Extract relevant product properties
        coffee_properties = {
            'name': name,
            'url': product_url
        }

        # Extract process, roast, origin, altitude, varietal, rest time, and price
        properties = {
            "process": "Process.",
            "roast": "Roast.",
            "location": "Origin.",
            "altitude": "Altitude.",
            "varietal": "Varietal.",
            "rest_time": "Rest Time."
        }

        for prop, label in properties.items():
            prop_tag = product_soup.find('p', string=label)
            if prop_tag:
                # Get the next sibling which contains the value
                value = prop_tag.find_next_sibling('p').text.strip()
                coffee_properties[prop] = value

        coffee_properties["price"] = product_soup.find('span', class_='price-item').text.strip()
        coffee_properties["description"] = product_soup.find('p', {"x-ref": "para"})['data-desc']

        # Append the coffee details to the list
        coffee_details.append(coffee_properties)


# Define the CSV file headers
headers = ["name", "url", "process", "roast", "location", "altitude", "varietal", "rest_time", "price","description"]

# Write the combined data to a CSV file
csv_filename = 'rossette.csv'
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