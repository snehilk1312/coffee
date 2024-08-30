import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

roaster = 'corridor_seven'
csv_file = 'corridor_seven.csv'
max_pages=3

# Function to scrape individual product page details
def scrape_product_details(product_url):
    response = requests.get(product_url)
    product_html_content = response.content
    product_soup = BeautifulSoup(product_html_content, 'html.parser')
    
    # Extract additional details
    description_div = product_soup.find('div', class_='shopify-product-details__short-description')
    if description_div:
        description_text = description_div.get_text(strip=True)
        description_parts = description_text.split('||')
        
        tastes_like = ""
        roasting_profile = ""
        varietal = ""
        altitude = ""
        process = ""
        estate_name = ""
        description = ""
        producer_name = ""
        
        for part in description_parts:
            if "Tastes Like" in part:
                tastes_like = part.replace("Tastes Like", "").strip().strip('-').strip()
            elif "Roasting Profile" in part:
                roasting_profile = part.replace("Roasting Profile", "").strip().strip('-').strip()
            elif "Varietal" in part:
                varietal = part.replace("Varietal", "").strip().strip('-').strip()
            elif "VARIETAL" in part:
                varietal = part.replace("VARIETAL", "").strip().strip('-').strip()
            elif "Altitude" in part:
                altitude = part.replace("Altitude", "").strip().strip('-').strip()
            elif "ALTITUDE" in part:
                altitude = part.replace("ALTITUDE", "").strip().strip('-').strip()
            elif "Process" in part:
                process = part.replace("Process", "").strip().strip('-').strip()
            elif "Estate Name" in part:
                estate_name = part.replace("Estate Name", "").strip().strip('-').strip()
            elif "Producer Name" in part:
                producer_name = part.replace("Producer Name", "").strip().strip('-').strip()
            elif "Profile" in part:
                roasting_profile = part.replace("Profile", "").strip().strip('-').strip()
            else:
                description = description_div.text
        
        return tastes_like, roasting_profile, varietal, altitude, process, estate_name, producer_name, description.strip()
    else:
        return None, None, None, None, None, None, None, None

# Function to scrape a single page of products
def scrape_page(page_url):
    response = requests.get(page_url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.find_all('div', class_='product-grid-item')
    
    product_data = []
    for product in products:
        name = product.find('h3', class_='product-title').get_text(strip=True)
        price = product.find('span', class_='price').get_text(strip=True)
        link = "https://corridorseven.coffee" + product.find('a', class_='jas-pr-image-link')['href']
        if name=='SAMPLER PACK':
            continue
        
        # Scrape additional details from individual product page
        tastes_like, roasting_profile, varietal, altitude, process, estate_name, producer_name, description = scrape_product_details(link)
        
        product_data.append([name, price, link, tastes_like, roasting_profile, varietal, altitude, process, estate_name, producer_name, description])
    
    return product_data

# Function to scrape all pages
def scrape_all_pages(base_url, max_pages):
    all_product_data = []
    
    for page_number in range(1, max_pages + 1):
        page_url = f"{base_url}?page={page_number}"
        print(f"Scraping {page_url}...")
        page_data = scrape_page(page_url)
        all_product_data.extend(page_data)
    
    return all_product_data

# Base URL of the product collection
base_url = "https://corridorseven.coffee/collections/all"

# Scrape data from all pages (replace 5 with the actual number of pages you want to scrape)
all_product_data = scrape_all_pages(base_url, max_pages)

# Write data to CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['Name', 'Price', 'Link', 'Tastes Like', 'Roasting Profile', 'Varietal', 'Altitude', 'Process', 'Estate Name', 'Producer Name', 'Description'])
    
    # Write product data
    writer.writerows(all_product_data)

print("Data has been written to corridor_seven_coffees.csv")

# putting it into db

conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
df = pd.read_csv(csv_file)
df['scraped_at'] = datetime.now()
df.to_sql(name = roaster , con=conn, index=False, if_exists='append',schema='raw_scraped')