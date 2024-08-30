import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

roaster = 'greysoul'

# Fetch homepage content
url = "https://greysoul.coffee/collections/coffee"
response = requests.get(url)
html_content = response.content

# Parse the homepage content
soup = BeautifulSoup(html_content, 'html.parser')
base_url = 'https://greysoul.coffee/'

# CSV setup
csv_file = 'coffee_greysoul.csv'
csv_columns = ['Name', 'Availability', 'Price', 'Link', 'Origin', 'Process', 'Varietal', 'Altitude', 
               'Dry Aroma', 'Wet Aroma', 'Roast Profile', 'Characteristics', 
               'Minimum Resting Period', 'Roaster Thoughts', 'About the Estate']

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_columns)

    for product in soup.find_all('li', class_='grid__item scroll-trigger animate--slide-in'):
        name = product.find('a', class_='full-unstyled-link').get_text(strip=True)
        price = product.find('span', class_='price-item--regular').get_text(strip=True)
        link = base_url + product.find('a', class_='full-unstyled-link')['href']
        availability = product.find('div', class_='card__badge').get_text(strip=True) if product.find('div', class_='card__badge') else 'Available'
        
        # Request individual product page
        product_response = requests.get(link)
        product_soup = BeautifulSoup(product_response.content, 'html.parser')
        
        # Extract additional properties from the table
        table = product_soup.find('table', border="1px")
        
        def extract_property(label):
            row = table.find('td', string=label)
            return row.find_next('td').get_text(strip=True) if row else 'N/A'

        origin = extract_property('Origin')
        process = extract_property('Process')
        varietal = extract_property('Varietal')
        altitude = extract_property('Altitude')
        dry_aroma = extract_property('Dry Aroma')
        wet_aroma = extract_property('Wet Aroma')
        roast_profile = extract_property('Roast Profile')
        characteristics = extract_property('Characteristics')
        min_resting_period = extract_property('Minimum resting period')

        # Extract Roaster Thoughts and About the Estate from divs
        roaster_thoughts = product_soup.find(string='Roaster thoughts :').find_next('span').get_text(strip=True) if product_soup.find(string='Roaster thoughts :') else None

        about_estate1 = product_soup.find(string='About the Estate :').find_next('p').get_text(strip=True) if product_soup.find(string='About the Estate :') else None
        about_estate2 = ' '.join(p.get_text(strip=True)  for p in product_soup.find(string='The estate and efforts:').find_all_next('span', limit=5)) if product_soup.find(string='The estate and efforts:') else None

        about_estate = about_estate1 if about_estate1 is not None else about_estate2


        # Write row to CSV
        writer.writerow([name, availability, price, link, origin, process, varietal, altitude, 
                         dry_aroma, wet_aroma, roast_profile, characteristics, 
                         min_resting_period, roaster_thoughts, about_estate])


# putting it into db

conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
df = pd.read_csv(csv_file)
df['scraped_at'] = datetime.now()
df.to_sql(name = roaster , con=conn, index=False, if_exists='append',schema='raw_scraped')