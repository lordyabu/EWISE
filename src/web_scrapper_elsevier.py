# -*- coding: utf-8 -*-
"""
Web Scapper for Academic Journals - Elsevier Module

This project provides a web scraping tool to extract data from academic 
journals, including article titles, authors, abstracts, and other details.
It uses the Python programming language and the Selenium library, 
along with the Firefox web driver, to automate the process of accessing 
academic journal webpages and collecting relevant information.

Those packages are built to search Elsevier papers.

"""

# =============================================================================
# Packages
# =============================================================================
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# =============================================================================
# Functions
# =============================================================================

# 1 - Get Url from different issues
def get_papers_link(url,html_list,wait_time):
    """
    This function retrieves the URLs of papers listed on a webpage using 
    Selenium and the Firefox web driver.
    
    Args:
        url (string): The URL of the webpage containing the list of papers.
        
        html_list (list): A list to store the extracted paper URLs.
        
        wait_time (TYPE): (float): The time to wait (in seconds) after loading 
        the webpage, allowing dynamic content to render before 
        extracting the links.

    Returns:
        html_list (list): A list containing the URLs of papers extracted from the webpage.

    """
    browser = webdriver.Firefox()
    browser.get(url)
    time.sleep(wait_time) 
    links = browser.find_elements(By.XPATH, "//h3/a")
    print(f"{len(links)} Links Found")
    for i in links:
        html_list.append(i.get_attribute('href'))
    browser.close()
    return html_list


# 2 - Get Abstract for a specific paper
def get_abstract_info(url_paper_list,paper_number,wait_time,title_id,author_id,abstract_id,issue_vol_id):
    """
    This function retrieves the abstract, title, authors, and issue/volume 
    information of a specific academic paper from a given list of URLs. 
    It uses Selenium and the Firefox web driver to access the webpage 
    containing the paper's details.

    Args:
        url_paper_list (list): A list containing URLs of academic papers' pages.
        
        paper_number (int): The index of the paper in url_paper_list from 
        which to retrieve the details.
        
        title_id (str): string with HTML id to paper's title.
        
        author_id (str): string with HTML id to paper's author.
        
        abstract_id (str): string with HTML id to paper's abstract.
        
        issue_vol_id (str): string with HTML id to paper's volume and issue.
        
        wait_time (float): The time to wait (in seconds) after loading 
        the webpage, allowing dynamic content to render before 
        extracting the links.

    Returns:
        paper (list): A list containing the issue/volume information as the 
        first element and a sublist with title, authors, and abstract as 
        the second element. If any exception occurs during scraping 
        (e.g., invalid URL, element not found), an empty list is returned.

    """
    try:
        browser = webdriver.Firefox()
        browser.get(url_paper_list[paper_number])
        time.sleep(wait_time)
        abstract = browser.find_element(By.ID, abstract_id).text
        title = browser.find_element(By.ID, title_id).text
        authors = browser.find_element(By.ID, author_id).text
        issue_volume = browser.find_element(By.ID, issue_vol_id).text
        paper = [issue_volume,[title,authors,abstract]]
    except: paper = []
    browser.close()
    return paper

# =============================================================================
# =============================================================================
