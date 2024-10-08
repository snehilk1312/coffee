import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

roaster = 'kapi_kottai'

# Base URL for links
base_url = "https://kapikottai.coffee"

# Extract product information
products = []

# Fetch webpage content
url = "https://kapikottai.coffee/collections/all?page="
num_pages = 3


for np in range(1,num_pages):
    url_scrape = url + str(np)
    response = requests.get(url_scrape)
    html_content = response.content
    # Parse the webpage content
    soup = BeautifulSoup(html_content, 'html.parser')

    for product in soup.find_all('li', class_='grid__item'):
        name = product.find('h3', class_='card__heading').get_text(separator=" ", strip=True)
        availability = product.find('div', class_='card__badge').get_text(separator=" ", strip=True)
        price = product.find('span', class_='price-item--regular').get_text(separator=" ", strip=True)
        link = base_url + product.find('a', class_='full-unstyled-link')['href']
    
        products.append([name, availability, price, link])

# Define a function to scrape properties from individual product pages
def scrape_properties(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialize a dictionary to store the properties
    properties = {
        "Origin": "",
        "Altitude": "",
        "Processing": "",
        "Tasting Notes": "",
        "Roast Level": "",
        "Description": ""
    }
    
    # Extract each property based on the specified HTML structure
    details = soup.find_all('details')
    for detail in details:
        summary = detail.find('summary')
        if summary:
            title = summary.get_text(separator=" ", strip=True)
            content = detail.find('div', class_='accordion__content rte')
            if content:
                property_value = content.get_text(separator=" ", strip=True)
                if title in properties:
                    properties[title] = property_value
    description = soup.find('div', class_='product__description')
    if description:
        properties['Description'] = description.get_text(separator=" ", strip=True)
    
    return properties

# Combine product information with detailed properties
detailed_products = []
for product in products:
    name, availability, price, link = product
    properties = scrape_properties(link)
    detailed_product = {
        "Product Name": name,
        "Availability": availability,
        "Price": price,
        "Link": link,
        **properties
    }
    detailed_products.append(detailed_product)

# Define the CSV file headers
headers = ["Product Name", "Availability", "Price", "Link", "Origin", "Altitude", "Processing", "Tasting Notes", "Roast Level", "Description"]

# Write the combined data to a CSV file
csv_filename = 'coffee_kapi_kottai.csv'
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