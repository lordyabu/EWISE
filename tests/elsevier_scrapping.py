# -*- coding: utf-8 -*-
"""
Web Scapper for Academic Journals

This project provides a web scraping tool to extract data from academic 
journals, including article titles, authors, abstracts, and other details.
It uses the Python programming language and the Selenium library, 
along with the Firefox web driver, to automate the process of accessing 
academic journal webpages and collecting relevant information.

"""
# =============================================================================
# Packages
# =============================================================================

# General Modules
import sys
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# Developed Modules
sys.path.append('C:\GIT privado\journal-web-scrapper\src')
from web_scrapper_elsevier import get_papers_link
from web_scrapper_elsevier import get_abstract

# =============================================================================
# Parameters
# =============================================================================

# 1 - URL with the journal issue and volume as paramter
journal_url = 'https://www.sciencedirect.com/journal/international-journal-of-forecasting/vol/{}/issue/{}'

# 2 - Start empty list with link for each paper
html_list = []
abstract_list = []

# 3 - Issues and Volumes availables
volumes = [35,36,37,38]
issues = [1,2,3,4]
url = []
	
# =============================================================================
# Application	
# =============================================================================

# 1 - Generate strings for each volume and issue
try:
    for volume in volumes:
        for issue in issues:
            url.append(journal_url.format(volume,issue))
except: pass


# 2 - Get links for each paper
try:
    for site in url:
        html_list = get_papers_link(site,html_list,5)   
except: pass
    

# 3 - Get Abstracts from step 2
try:
    for i in range(1,len(html_list)):
        abstract = get_abstract(html_list,i,5)
        abstract_list.append(abstract)
except: pass

# =============================================================================
# =============================================================================
    
    
    
    
    
    
    
    
    
    
    

