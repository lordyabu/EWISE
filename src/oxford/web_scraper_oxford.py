# -*- coding: utf-8 -*-

"""
Web Scraper for Academic Journals - Oxford Module

This module provides a web scraping tool to extract data from academic journals published by Oxford.
It automates the process of accessing journal webpages and collecting information such as article titles,
authors, abstracts, and issue/volume details using Python, Selenium, and the Firefox web driver.
The tool is designed to assist in gathering data for academic research and analysis.

Functions:
    get_papers_link_oxford(url, html_list, wait_time): Retrieves URLs of papers from a specified Oxford journal webpage.
    get_abstract_info_oxford(url_paper_list, paper_number, wait_time): Extracts detailed information from a Oxford paper's webpage,
        including abstract, title, authors, and issue/volume information.

Usage:
    1. Collect paper URLs:
        paper_urls = get_papers_link_oxford(journal_url, [], wait_time)

    2. Extract paper details:
        paper_info = get_abstract_info_oxford(paper_urls, paper_index, wait_time)
"""

# =============================================================================
# Packages
# =============================================================================
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from config import GECKO_PATH
import re
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =============================================================================
# Functions
# =============================================================================

def get_papers_link_oxford(url, wait_time):
    """
    Retrieves URLs of papers from a specified Oxford journal webpage.

    Args:
        url (str): URL of the journal's webpage.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        paper_links (list): List of URLs of papers.
    """
    # Initialize the browser
    service = Service(GECKO_PATH)
    browser = webdriver.Firefox(service=service)
    browser.get(url)

    # Wait for the page to render
    time.sleep(wait_time)

    # Find all elements that match the desired XPath
    articles = browser.find_elements(By.XPATH, "//h5[@class='customLink item-title']/a")

    # Initialize a list to store the full URLs
    paper_links = []

    # Construct the full URL for each paper and add it to the list
    base_url = "https://academic.oup.com"

    for article in articles:
        partial_link = article.get_attribute('href')
        full_link = base_url + partial_link if partial_link.startswith("/doi") else partial_link
        paper_links.append(full_link)

    # Close the browser
    browser.close()

    return paper_links


def get_abstract_info_oxford(url_paper_list, paper_number, wait_time):
    """
    Retrieves detailed information of a specific paper from Oxford.

    Args:
        url_paper_list (list): List of paper URLs.
        paper_number (int): Index of the paper in the list.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        paper (list): A list containing detailed information of the paper.
    """
    paper = []
    try:
        service = Service(GECKO_PATH)
        browser = webdriver.Firefox(service=service)
        browser.get(url_paper_list[paper_number])

        # Wait for the page to render
        time.sleep(wait_time)

        # Find the title
        title = browser.find_element(By.CSS_SELECTOR, "h1.wi-article-title").text

        # Find the authors
        authors_elements = browser.find_elements(By.CSS_SELECTOR, "div.wi-authors span.al-author-name-more button.linked-name")
        authors = ", ".join([author.text for author in authors_elements])

        # Find the abstract
        abstract = browser.find_element(gfBy.CSS_SELECTOR, "section.abstract p").text

        # Find the volume and issue
        volume = browser.find_element(By.CSS_SELECTOR, "div.volume-issue__wrap .volume").text
        issue = browser.find_element(By.CSS_SELECTOR, "div.volume-issue__wrap .issue").text
        issue_volume = f"{volume}, {issue}"

        paper = [issue_volume, [title, authors, abstract]]
    except Exception as e:
        paper = ["Error: " + str(e)]

    finally:
        browser.close()

    return paper

