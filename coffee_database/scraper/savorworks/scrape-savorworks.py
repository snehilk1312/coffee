import requests
from bs4 import BeautifulSoup
import csv

# Fetch homepage content
url = "https://www.savorworksroasters.com/collections/coffee"
response = requests.get(url)
html_content = response.content

# Parse HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract product information
products = []
for item in soup.find_all('div', class_='m-product-item'):
    name = item.find('a', class_='m-product-card__name').text.strip()
    price = item.find('span', class_='m-price-item m-price-item--regular').text.strip()
    link = "https://www.savorworksroasters.com" + item.find('a', class_='m-product-card__link')['href']
    
    products.append([name, price, link])

# Function to extract details from HTML
def scrape_properties(url):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the Description
    description = soup.find('div', class_= 'm-tab-content--description').get_text(separator=' ', strip=True)
    
    # Find the facts section
    facts = soup.find('div', class_='rte').find_all('p')
    # print(facts)
    
    # Extract each fact
    properties_temp = {
    "Origin" : '',
    "Altitude" : '',
    "Varietal"  : '',
    "Process"  : '',
    "Tasting Notes"  : '',
    "Acidity"  : '',
    "Body"  : '',
    "Aftertaste"  : '',
    "Roast Rite Color (Whole Bean)"  : '',
    "Roast Rite Color (Ground)"  : '',
    "Roast Level"  : ''}

    properties={}

    for fact in facts:
        fact_text = fact.get_text(separator=' ', strip=True)

        fact_text = fact_text.replace('Estate:','Origin:')
        fact_text = fact_text.replace(' ( ',' (')

        for title in properties_temp.keys():
            if len(fact_text.split(title))>1:
                properties[title] = fact_text.split(title)[1].strip().strip(':').strip().strip('-').strip()
                for title_inner in properties_temp.keys():
                    if len(properties[title].split(title_inner))>1:
                        properties[title] = properties[title].split(title_inner)[0]
    properties['description'] = description

    return properties

# Combine product information with detailed properties
detailed_products = []
for product in products:
    name, price, link = product
    properties = scrape_properties(link)
    detailed_product = {
        "name": name,
        "price": price,
        "link": link,
        **properties
    }
    detailed_products.append(detailed_product)

# Define the CSV file headers
headers = ["name","price", "link", "Origin", "Altitude", "Varietal", "Process", "Tasting Notes","Acidity","Body","Aftertaste","Roast Rite Color (Whole Bean)","Roast Rite Color (Ground)","Roast Level","description"]

# Write the combined data to a CSV file
csv_filename = 'coffee_savorworks.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for row in detailed_products:
        writer.writerow(row)

print(f"Data saved to {csv_filename}")