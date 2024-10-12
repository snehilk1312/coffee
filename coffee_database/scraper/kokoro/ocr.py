import requests
from PIL import Image, ImageFilter
import pytesseract
from io import BytesIO

# The URL of the image
image_url = 'https://kokoro.in/Office/assets/Documents/Product/Cover_20240923_2e2129b4-4b12-4c56-ad37-551f466fccf1.png'

# Download the image
response = requests.get(image_url)
if response.status_code == 200:
    image_data = BytesIO(response.content)  # Convert the content to a BytesIO object
    image = Image.open(image_data)  # Open the image with PIL
    
    # Convert to grayscale and sharpen
    image = image.convert('L')
    image = image.filter(ImageFilter.SHARPEN)

    # Perform OCR using pytesseract
    extracted_text = pytesseract.image_to_string(image)

    # Output the extracted text
    print(extracted_text)
else:
    print(f"Failed to retrieve the image. Status code: {response.status_code}")
