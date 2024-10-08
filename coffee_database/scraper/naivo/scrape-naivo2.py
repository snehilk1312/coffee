from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the webdriver
driver = webdriver.Chrome()

# Go to the URL
url = "https://naivo.in/product-category/all-coffee/"
driver.get(url)

# Allow the page to load fully
time.sleep(5)

# Scrape the coffee product names and links
coffee_names = driver.find_elements(By.CSS_SELECTOR, 'h2.woocommerce-loop-product__title')
coffee_links = driver.find_elements(By.CSS_SELECTOR, 'a.usg_btn_1')
# Extract names and links
coffees = []
for _ in range(len(coffee_names)):
    coffee_name = coffee_names[_].text
    coffee_link = coffee_links[_].get_attribute('href')
    coffees.append((coffee_name, coffee_link))

# Close the driver
driver.quit()

# Print the result
for coffee in coffees:
    print(f"Coffee Name: {coffee[0]}, Link: {coffee[1]}")
