import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os,json,re
from dotenv import load_dotenv

load_dotenv()

roaster = 'kc_roasters'

url = "https://kcroasters.com/collections/coffee"
response = requests.get(url)
html_content = response.content

def remove_spaces_around_special_chars(s):
    return re.sub(r'\s*([^\w\s])\s*', r'\1', s)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all product entries
products = soup.find_all('script', type='application/ld+json')

extracted_data = []
for product in products:
    product_data = product.string
    if'"@type" : "Product"'in product_data:
        product_json = json.loads(product_data)

        # Extract the required fields
        for j in range(len(product_json)):
            url = product_json[j].get('url', '')
            name = product_json[j].get('name', '')
            price = str(product_json[j].get('offers', ''))
            if price:
                price = price.split("'price': ")[1].split(',')[0]
            description = product_json[j].get('description', '').lower()
            description = description.replace(':','-')
            description = remove_spaces_around_special_chars(description)

            # Extract properties from the description
            region = ''
            process = ''
            altitude = ''
            best_with = ''
            tasting_notes = ''

            description_text = description

            # Find each property in the description
            if 'region-' in description:
                region = description.split('region-')[1].split('process-')[0].strip()
            if 'process-' in description:
                process = description.split('process-')[1].split('altitude-')[0].strip()
            if 'altitude-' in description:
                altitude = description.split('altitude-')[1].split('best with-')[0].strip()
            if 'best with-' in description:
                best_with = description.split('best with-')[1].split('notes-')[0].strip()
            if "notes-" in description:
                tasting_notes = description.split('notes-')[1].split('note-')[0].strip()

            # Append the data to the list
            extracted_data.append([url, name, description_text, region, process, altitude, best_with, tasting_notes,price])

# Write to CSV file
csv_file = 'kcroasters_extracted_data.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Write the header row
    writer.writerow(['URL', 'Name', 'Description', 'Region', 'Process', 'Altitude', 'Best with', 'Tasting Notes','Price'])
    # Write the extracted data rows
    writer.writerows(extracted_data[1:])

print(f"Data has been successfully written to {csv_file}")


# putting it into db

conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
df = pd.read_csv(csv_file)
df['scraped_at'] = datetime.now()
df.to_sql(name = roaster , con=conn, index=False, if_exists='replace',schema='raw_scraped')