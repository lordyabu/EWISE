# -*- coding: utf-8 -*-

"""
Web Scraper for Academic Journals - Elsevier Module

This module provides a web scraping tool for extracting data from academic journals published by Elsevier.
It automates the process of accessing journal webpages and collecting information like article titles,
authors, abstracts, and issue/volume details using Python, Selenium, and the Firefox web driver.
The scraped data is structured for easy analysis and research purposes.

Functions:
    get_papers_link_econometrica(url, html_list, wait_time): Scrapes URLs of papers listed on a journal's webpage.
    get_abstract_info_econometrica(url_paper_list, paper_number, wait_time, vol_issue): Extracts detailed information
        from a paper's webpage, including abstract, title, authors, and issue/volume information.

Usage:
    1. To collect paper URLs:
        paper_urls = get_papers_link_econometrica(journal_url, [], wait_time)

    2. To extract details of a specific paper:
        paper_details = get_abstract_info_econometrica(paper_urls, paper_index, wait_time, vol_issue_list)
"""

# =============================================================================
# Packages
# =============================================================================
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from config import GECKO_PATH


# =============================================================================
# Functions
# =============================================================================
def get_papers_link_econometrica(url, html_list, wait_time):
    """
    Retrieves URLs of papers from a specified Econometrica journal webpage.

    Args:
        url (str): URL of the journal's webpage.
        html_list (list): List to store the paper URLs.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        tuple: Updated html_list with URLs, and the number of new URLs added.
    """
    html_list_start_len = len(html_list)

    service = Service(GECKO_PATH)
    browser = webdriver.Firefox(service=service)
    browser.get(url)
    time.sleep(wait_time)
    # Find all article links based on the class name
    links = browser.find_elements(By.CSS_SELECTOR, "a.issue-item__title.visitable")
    for link in links:
        html_list.append(link.get_attribute('href'))

    browser.close()

    html_list_end_len = len(html_list)
    return html_list, html_list_end_len - html_list_start_len


def get_abstract_info_econometrica(url_paper_list, paper_number, wait_time, vol_issue):
    """
    Retrieves detailed information of a specific paper from Econometrica.

    Args:
        url_paper_list (list): List of paper URLs.
        paper_number (int): Index of the paper in the list.
        wait_time (int): Time to wait for page rendering before scraping.
        vol_issue (list): List containing issue/volume information for each paper.

    Returns:
        paper (list): A list with issue/volume information and a sublist with title, authors, and abstract.
    """
    try:
        service = Service(GECKO_PATH)
        browser = webdriver.Firefox(service=service)
        browser.get(url_paper_list[paper_number])
        time.sleep(wait_time)
        abstract = browser.find_element(By.CSS_SELECTOR, "div.article-section__content.en.main").text
        title = browser.find_element(By.CLASS_NAME, "citation__title").text
        issue_volume = vol_issue[paper_number]
        author_elements = browser.find_elements(By.CLASS_NAME, "author-name")
        authors = [author_element.text for author_element in author_elements if author_element.text.strip()]
        paper = [issue_volume, [title, authors, abstract]]

    except Exception as e:
        paper = []

    browser.close()
    return paper
