import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

roaster = 'half_light'

# Fetch homepage content
url = "https://halflightcoffee.com/collections/coffee"
response = requests.get(url)
html_content = response.content

# Parse the homepage content
soup = BeautifulSoup(html_content, 'html.parser')
base_url = 'https://halflightcoffee.com'

coffee_details = []
# 


for product in soup.find_all('div',class_='product__details'):
    link_tag = product.find('a', href=True,class_='hidden-product-link')
    
    if link_tag:
        name = link_tag.get_text(strip=True)
        product_url = base_url + link_tag['href']  # Construct the full URL

        # Fetch the individual product page to extract additional details
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.content.lower(), 'html.parser')
        price = product_soup.find('div',class_='modal_price').get_text(separator=" ", strip=True)
        

        prop_tag = product_soup.find('div', class_='description bottom')
        description = prop_tag.get_text(separator=" ", strip=True)

        properties_list = ['location','altitude','varietal','process','cup notes','roast profile']

        coffee_properties = {
            'name': name,
            'url': product_url,
            'description': description,
            'price': price
            }

        for prop in properties_list:
            try:
                coffee_properties[prop] = prop_tag.find('strong', string=lambda x: prop in x).get_text(strip=True).split(prop)[-1].strip().strip('–').strip('-').strip()
            except Exception as e:
                coffee_properties[prop] = None
                # print(e)



        coffee_details.append(coffee_properties)


# Define the CSV file headers
headers = ["name", "url", "price","description",'location','altitude','varietal','process','cup notes','roast profile']

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