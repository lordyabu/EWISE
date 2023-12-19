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
import warnings
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service
from config import GECKO_PATH
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =============================================================================
# Functions
# =============================================================================



def get_volume_and_issue_data_aea(url):
    service = Service(GECKO_PATH)
    browser = webdriver.Firefox(service=service)
    base_url = "https://www.aeaweb.org"
    browser.get(url)

    # Dictionary to store volume: [(issue_number, link)]
    volume_dict = {}

    # Find all volume elements
    volume_elements = browser.find_elements(By.CLASS_NAME, "volume-container")

    for volume_element in volume_elements:
        volume_label = volume_element.find_element(By.CLASS_NAME, "volume-label").text
        volume = volume_label.split('—')[1].strip()  # Extract volume number

        issue_elements = volume_element.find_elements(By.CLASS_NAME, "issue-item")

        issue_list = []
        issue_num = 4  # Start with the highest issue number
        for issue in issue_elements:
            issue_link_element = issue.find_element(By.TAG_NAME, "a")
            link = issue_link_element.get_attribute('href')
            full_link = base_url + link if not link.startswith('http') else link

            issue_list.append((str(issue_num), full_link))
            issue_num -= 1  # Decrease the issue number for the next issue

        volume_dict[volume] = issue_list
    browser.close()
    return volume_dict

# 1 - Get Url from different issues
def get_papers_link_aea(url, html_list, wait_time):
    """
    This function retrieves the URLs of papers listed on a webpage using
    Selenium and the Firefox web driver.

    Args:
        url (string): The URL of the webpage containing the list of papers.
        html_list (list): A list to store the extracted paper URLs.
        wait_time (float): The time to wait (in seconds) after loading
                           the webpage, allowing dynamic content to render before
                           extracting the links.

    Returns:
        html_list (list): A list containing the URLs of papers extracted from the webpage.
    """
    time.sleep(wait_time)
    service = Service(GECKO_PATH)
    browser = webdriver.Firefox(service=service)
    browser.get(url)
    time.sleep(wait_time)

    # Find all article links based on the updated structure
    articles = browser.find_elements(By.CSS_SELECTOR, "article.journal-article h3.title a")
    for article in articles:
        html_list.append(article.get_attribute('href'))

    browser.close()
    return html_list


# 2 - Get Abstract for a specific paper


# =============================================================================
# =============================================================================
def get_abstract_info_aea(url_paper_list, paper_number, wait_time):
    """
    This function retrieves the abstract, title, authors, and issue/volume
    information of a specific academic paper from a given list of URLs.
    It uses Selenium and the Firefox web driver to access the webpage
    containing the paper's details.

    Args:
        url_paper_list (list): A list containing URLs of academic papers' pages.
        paper_number (int): The index of the paper in url_paper_list from
                            which to retrieve the details.
        wait_time (float): The time to wait (in seconds) after loading
                           the webpage, allowing dynamic content to render before
                           extracting the information.

    Returns:
        paper (list): A list containing the issue/volume information as the
                      first element and a sublist with title, authors, and abstract as
                      the second element. If any exception occurs during scraping
                      (e.g., invalid URL, element not found), an empty list is returned.

    """
    try:
        time.sleep(wait_time)
        service = Service(GECKO_PATH)
        browser = webdriver.Firefox(service=service)
        browser.get(url_paper_list[paper_number])
        time.sleep(wait_time)

        # Extract the abstract, title, and authors
        abstract = browser.find_element(By.CSS_SELECTOR, "section.article-information.abstract").text
        title = browser.find_element(By.CSS_SELECTOR, "h1.title").text
        authors = [author.text for author in browser.find_elements(By.CSS_SELECTOR, "ul.attribution li.author")]
        # Extract the issue and volume information
        issue_volume_info = browser.find_element(By.CSS_SELECTOR, "div.journal").text
        paper = [issue_volume_info, [title, authors, abstract, 'Metrics NA']]

    except Exception as e:
        print(f"An error occurred: {e}")
        paper = []

    browser.close()
    return paper