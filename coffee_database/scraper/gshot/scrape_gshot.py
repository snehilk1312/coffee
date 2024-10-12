import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

roaster = 'gshot'

# Fetch homepage content
url = "https://gshotcoffeeroastery.com/collections/coffee"
response = requests.get(url)
html_content = response.content

# Parse the homepage content
soup = BeautifulSoup(html_content, 'html.parser')
base_url = 'https://gshotcoffeeroastery.com'

coffee_details = []

for product_link in soup.find_all('a',class_='thumbnail__link'):
    product_url = base_url + product_link['href']  # Construct the full URL
    
    product_response = requests.get(product_url)
    product_soup = BeautifulSoup(product_response.content.lower(), 'html.parser')

    # Scraping the product name
    product_name = product_soup.find('h1', class_='product_name').get_text(strip=True)
    if product_name=='project sarada - sampler pack!':
        continue

    # Scraping the product price
    price = product_soup.find('span', class_='current_price').get_text(strip=True)

    # Scraping the product description details
    description_block = product_soup.find('div', class_='product-block--description__text').get_text(separator=" ", strip=True)


    # Extracting specific details from the description
    details = {
        "name": product_name,
        "price": price,
        "url": product_url,
        "estate": None,
        "location": None,
        "altitude": None,
        "varietal": None,
        "process": None,
        "roast_level": None,
        "tasting_notes":None,
        "description": description_block
    }


    for strong_tag in product_soup.find('div', class_='product-block--description__text').find_all('strong'):
        text = strong_tag.get_text(strip=True)
        if "estate" in text:
            details['estate'] = strong_tag.next_sibling.strip().strip(':').strip('-').strip('–').strip()
        elif "region" in text:
            details['location'] = strong_tag.next_sibling.strip().strip(':').strip('-').strip('–').strip()
        elif "altitude" in text:
            details['altitude'] = strong_tag.next_sibling.strip().strip(':').strip('-').strip('–').strip()
        elif "varietal" in text:
            details['varietal'] = strong_tag.next_sibling.strip().strip(':').strip('-').strip('–').strip()
        elif "process" in text:
            details['process'] = strong_tag.next_sibling.strip().strip(':').strip('-').strip('–').strip()
        elif "roast style" in text:
            details['roast_level'] = strong_tag.next_sibling.strip().strip(':').strip('-').strip('–').strip()
        elif "tasting notes" in text:
            details['tasting_notes'] = text.split('–')[-1].split('-')[-1].split(':')[-1].strip().strip('-').strip('–').strip()
        elif "flavour notes" in text:
            details['tasting_notes'] = strong_tag.next_sibling.strip().strip(':').strip('-').strip('–').strip()

    if not details['estate'] and 'araku' in details['location']:
        details['estate'] = 'araku'

    coffee_details.append(details)

# Define the CSV file headers
headers = ["name","price","url",'estate','location','altitude','varietal','process','roast_level',"tasting_notes","description"]

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