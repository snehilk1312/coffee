import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv
from PIL import Image, ImageFilter
import pytesseract
from io import BytesIO
load_dotenv()

roaster = 'kokoro'

# Fetch homepage content
url = "https://kokoro.in/Office/assets/Documents/Product/"
response = requests.get(url)
html_content = response.content

# Parse the homepage content
soup = BeautifulSoup(html_content, 'html.parser')
base_url = 'https://kokoro.in'

coffee_details = []

num = 0
for img_link in soup.find_all('a'):
    if img_link['href']=="/Office/assets/Documents/":
        continue
    image_url = base_url+img_link['href']


    response = requests.get(image_url)

    if response.status_code == 200:
        image_data = BytesIO(response.content)  # Convert the content to a BytesIO object
        image = Image.open(image_data)  # Open the image with PIL

        # Save (download) the image
        # try:
        #     image.save(f'{num}.jpeg')  # Saves the image locally
        # except:
        #     image.save(f'{num}.png')  # Saves the image locally

        # Convert to grayscale and sharpen
        image = image.convert('L')
        image = image.filter(ImageFilter.SHARPEN)

        # Perform OCR using pytesseract
        extracted_text = pytesseract.image_to_string(image)

        # Output the extracted text
        if extracted_text:
            print(extracted_text)
            print('*'*100)
    else:
        print(f"Failed to retrieve the image. Status code: {response.status_code}")
    
    num+=1
