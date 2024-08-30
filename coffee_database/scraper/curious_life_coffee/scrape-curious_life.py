import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

roaster = 'curious_life'

# Fetch homepage content
url = "https://curiouslifecoffee.com/store"
response = requests.get(url)
html_content = response.content

# Parse HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# CSV file setup
csv_file = "coffee_curious_life.csv"
csv_columns = ["Name", "Price", "Link", "Varietal", "Processing", "Country", "Region", "Altitude", "Farmer", "Roast", "Description"]

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(csv_columns)

    # Extract product information from the main page
    for product in soup.find_all('li', class_='isotope-item'):
        name = product.find('h4').text.strip()
        price = product.find('div', class_='prod-price').text.strip()
        link = product.find('a', href=True)['href']

        # Fetch individual product page content
        product_response = requests.get(link)
        product_html_content = product_response.content
        product_soup = BeautifulSoup(product_html_content, 'html.parser')

        # Extract additional product details
        details = product_soup.find('div', class_='wpb_wrapper')
        rows = details.find_all('tr')
        product_details = {}

        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                key = cols[0].text.replace(":", "").strip()
                value = cols[1].text.strip()
                product_details[key] = value

        # Extract the description text
        description_div = product_soup.find('div', class_='wpb_text_column wpb_content_element txt-justify')
        description = description_div.get_text(separator=" ", strip=True) if description_div else ""

        # Collect all the data
        row_data = [
            name, price, link,
            product_details.get("Varietal", ""),
            product_details.get("Processing", ""),
            product_details.get("Country", ""),
            product_details.get("Region", ""),
            product_details.get("Altitude", ""),
            product_details.get("Farmer", ""),
            product_details.get("Roast", ""),
            description
        ]

        # Write to CSV
        writer.writerow(row_data)

print(f"Data scraped and saved to {csv_file}")


# putting it into db

conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
df = pd.read_csv(csv_file)
df['scraped_at'] = datetime.now()
df.to_sql(name = roaster , con=conn, index=False, if_exists='append',schema='raw_scraped')