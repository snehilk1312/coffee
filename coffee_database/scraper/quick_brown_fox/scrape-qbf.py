import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os,re
from dotenv import load_dotenv

load_dotenv()

roaster = 'quick_brown_fox'



# Define the base URL
base_url = "https://qbfcoffee.com"

# Fetch homepage content
url = f"{base_url}/collections/all-coffees"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

csv_filename = 'coffee_qbf.csv'
# Prepare the CSV file
csv_file = open(csv_filename, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow([
    'Name', 'Price', 'Link', 
    'Tasting Notes', 'Roast', 'Location', 
    'Elevation', 'Varietal', 'Process', 
    'Fermentation', 'Farmer','Description'
])

# Extract product details from the homepage
products = soup.find_all('div', class_='grid-view-item')

for product in products:
    # Extract the product name
    name = product.find('div', class_='h4 grid-view-item__title').text.strip()
    
    # Extract the product price
    price = product.find('span', class_='product-price__price').text.strip()
    
    # Extract the product link
    relative_link = product.find('a', class_='grid-view-item__link')['href']
    product_link = f"{base_url}{relative_link}"
    
    # Fetch product detail page content
    product_response = requests.get(product_link)
    product_html_content = product_response.content
    product_soup = BeautifulSoup(product_html_content, 'html.parser')
    
    # Extract additional details
    description_section = product_soup.find('div', class_='product-single__description rte')
    content = description_section.decode_contents()

    # Split on <br/>, <br>, or newline (\n)
    lines = re.split(r'<br\s*/?>|\n', content)
    lines = [i.replace('\xa0','') for i in lines]
    properties = {}

    for line in lines:
        # Remove leading/trailing spaces and any remaining HTML tags
        clean_line = BeautifulSoup(line.strip(), 'html.parser').text.lower()
        if " -" in clean_line:
            key, value = clean_line.split(" -", 1)
            properties[key.strip()] = value.strip()
        elif ":" in clean_line:
            key, value = clean_line.split(":", 1)
            properties[key.strip()] = value.strip()


    tasting_notes = properties.get('tasting notes')
    roast = properties.get('roast level') if properties.get('roast level') else properties.get('roast')
    location = properties.get('location')
    elevation = properties.get('elevation') if properties.get('elevation') else properties.get('altitude')
    varietal = properties.get('varietal')
    process = properties.get('process')
    fermentation = properties.get('fermentation')
    farmer = properties.get('farmer')
    description = description_section.get_text(strip=True,separator=' ')

    # Write to CSV
    csv_writer.writerow([
        name, price, product_link, 
        tasting_notes, roast, location, 
        elevation, varietal, process, 
        fermentation,farmer, description
    ])

csv_file.close()


# putting it into db

conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
df = pd.read_csv(csv_filename)
df['scraped_at'] = datetime.now()
df.to_sql(name = roaster , con=conn, index=False, if_exists='append',schema='raw_scraped')