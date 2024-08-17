from bs4 import BeautifulSoup
import json
import csv
import requests
import re

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

            # Remove the properties from the description text
            description_text = description.split('region-')[0].strip()

            # Append the data to the list
            extracted_data.append([url, name, description_text, region, process, altitude, best_with, tasting_notes])

# Write to CSV file
csv_file = 'kcroasters_extracted_data.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Write the header row
    writer.writerow(['URL', 'Name', 'Description', 'Region', 'Process', 'Altitude', 'Best with', 'Tasting Notes'])
    # Write the extracted data rows
    writer.writerows(extracted_data[1:])

print(f"Data has been successfully written to {csv_file}")