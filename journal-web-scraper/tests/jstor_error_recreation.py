from selenium.webdriver.chrome.service import Service as ServiceC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from config import CHROME_PATH
from selenium import webdriver
import time

url = 'https://www.jstor.org/journal/jecongrowth'

# Initialize the Chrome WebDriver
service = ServiceC(CHROME_PATH)
browser = webdriver.Chrome(service=service)

# Go to the specified URL
browser.get(url)

# Wait for the page to load completely. Adjust the sleep time as needed
time.sleep(30)

# Scroll to the bottom of the page to ensure all content is loaded
# This may need to be done several times if the page loads content dynamically as you scroll
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(30)

# Get the page source and close the browser
page_source = browser.page_source

browser.quit()

# Use BeautifulSoup to parse the page source
soup = BeautifulSoup(page_source, 'html.parser')

print(soup)

# Find all collection-view-pharos-link tags containing '/stable' in the 'href'
stable_links = soup.find_all('collection-view-pharos-link', href=lambda href: href and '/stable' in href)

# Extract the href attributes
links = [link['href'] for link in stable_links if 'href' in link.attrs]

# Print the extracted links
for link in links:
    print(link)
