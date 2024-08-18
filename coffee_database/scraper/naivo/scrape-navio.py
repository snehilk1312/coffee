import csv
from bs4 import BeautifulSoup
import requests

# Base URL for the website
base_url = "https://naivo.in/product-category/shop-coffee/page/"
total_pages = 3

# Open CSV file for writing
with open('coffee_naivo.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the headers
    writer.writerow([
        'Name of Coffee', 'Price', 'Producers', 'Region', 'Type', 
        'Roast Profile', 'Altitude', 'Process', 'Varieties', 'Flavor Notes', 'Description', 'Link'
    ])
    
    # Loop through multiple pages
    for page_num in range(1, total_pages+1):  # Adjust the range according to the number of pages
        # Construct the URL for each page
        url = f"{base_url}{page_num}"
        
        # Fetch page content
        response = requests.get(url)
        html_content = response.content
        html_content = html_content.lower()

        soup = BeautifulSoup(html_content, 'html.parser')

        # Loop through each coffee product block
        for article in soup.find_all('article', class_='product-item-wrap'):
            # Extract the name of the coffee
            name_tag = article.find('h4', class_='product-name')
            name = name_tag.text.strip() if name_tag else "N/A"

            # Extract the price
            price_tag = article.find('span', class_='woocommerce-price-amount')
            price = price_tag.text.strip() if price_tag else "N/A"
            
            # Extract the link of the coffee product
            link_tag = article.find('a', href=True)
            link = link_tag['href'] if link_tag else "N/A"

            # Extract additional details from the product description
            description_list = article.find('div', class_='product-description')
            if description_list:
                items = description_list.find_all('li')
                producers = items[0].text.split(":")[1].strip() if len(items) > 0 else "N/A"
                region = items[1].text.split(":")[1].strip() if len(items) > 1 else "N/A"
                coffee_type = items[2].text.split(":")[1].strip() if len(items) > 2 else "N/A"
                roast_profile = items[3].text.split(":")[1].strip() if len(items) > 3 else "N/A"
                altitude = items[4].text.split(":")[1].strip() if len(items) > 4 else "N/A"
                process = items[5].text.split(":")[1].strip() if len(items) > 5 else "N/A"
                varieties = items[6].text.split(":")[1].strip() if len(items) > 6 else "N/A"
                flavor_notes = items[7].text.split(":")[1].strip() if len(items) > 7 else "N/A"
            else:
                producers = region = coffee_type = roast_profile = altitude = process = varieties = flavor_notes = "N/A"

            # Extract the product description
            description_paragraphs = article.find_all('p')
            description = " ".join([p.text.strip() for p in description_paragraphs])

            # Write the coffee details to the CSV, including the link
            writer.writerow([
                name, price, producers, region, coffee_type, roast_profile,
                altitude, process, varieties, flavor_notes, description, link
            ])

print("Coffee details extracted and saved to coffee_naivo.csv")
