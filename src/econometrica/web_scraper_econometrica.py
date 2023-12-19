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
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from config import GECKO_PATH


# =============================================================================
# Functions
# =============================================================================

# 1 - Get Url from different issues
def get_papers_link_econometrica(url, html_list, wait_time):
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
    service = Service(GECKO_PATH)
    browser = webdriver.Firefox(service = service)
    browser.get(url)
    time.sleep(wait_time)
    # Find all article links based on the class name
    links = browser.find_elements(By.CSS_SELECTOR, "a.issue-item__title.visitable")
    for link in links:
        html_list.append(link.get_attribute('href'))

    browser.close()
    return html_list


# 2 - Get Abstract for a specific paper


# =============================================================================
# =============================================================================
def get_abstract_info_econometrica(url_paper_list, paper_number, wait_time):
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
        service = Service(GECKO_PATH)
        browser = webdriver.Firefox(service=service)
        browser.get(url_paper_list[paper_number])
        time.sleep(wait_time)
        abstract = browser.find_element(By.CSS_SELECTOR, "div.article-section__content.en.main").text
        title = browser.find_element(By.CLASS_NAME, "citation__title").text
        issue_volume = "Econometrica" # ToDo Find somewhere on the page, but if it's just this it works fine
        author_elements = browser.find_elements(By.CLASS_NAME, "author-name")
        authors = [author_element.text for author_element in author_elements if author_element.text.strip()]

        try:
            metrics_data = browser.find_element(By.CSS_SELECTOR, "div.epub-section.cited-by-count a").text
        except:
            metrics_data = 0
        paper = [issue_volume, [title, authors, abstract, metrics_data]]
    except Exception as e:
        paper = []

    browser.close()
    return paper