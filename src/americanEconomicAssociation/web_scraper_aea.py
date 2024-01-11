# -*- coding: utf-8 -*-
"""
Web Scraper for Academic Journals - AEA Module

This module provides a web scraping tool to extract data from academic journals published by the American Economic Association (AEA).
It automates the process of accessing journal webpages and collecting information like article titles, authors, abstracts,
and issue/volume details. The tool uses Python, Selenium, and BeautifulSoup along with the Firefox web driver for scraping.
The extracted data is collected in a structured format.

Functions:
    get_volume_and_issue_data_aea(url): Retrieves volume and issue data for a specified AEA journal.
    get_papers_link_aea(url, html_list, wait_time): Collects paper URLs from a journal's webpage.
    get_abstract_info_aea(url_paper_list, paper_number, wait_time): Extracts abstract, title, authors,
        and issue/volume information from a paper's webpage.

Usage:
    1. Retrieve volume and issue data:
        volume_issue_data = get_volume_and_issue_data_aea(journal_url)

    2. Collect paper URLs:
        paper_urls = get_papers_link_aea(journal_url, [], wait_time)

    3. Extract paper details:
        paper_info = get_abstract_info_aea(paper_urls, paper_index, wait_time)
"""

# =============================================================================
# Packages
# =============================================================================
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from config import GECKO_PATH
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =============================================================================
# Functions
# =============================================================================
def get_volume_and_issue_data_aea(url):
    """
    Retrieves volume and issue data from the specified AEA journal URL.

    Args:
        url (str): URL of the AEA journal page to scrape.

    Returns:
        volume_dict (dict): A dictionary mapping each volume to its issues and corresponding URLs.
    """

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
        issue_num = 4  # Start with the highest issue number (All journals follow 4, 3, 2, 1) pattern
        for issue in issue_elements:
            issue_link_element = issue.find_element(By.TAG_NAME, "a")
            link = issue_link_element.get_attribute('href')
            full_link = base_url + link if not link.startswith('http') else link

            issue_list.append((str(issue_num), full_link))
            issue_num -= 1  # Decrease the issue number for the next issue

        volume_dict[volume] = issue_list
    browser.close()
    return volume_dict


def get_papers_link_aea(url, html_list, wait_time):
    """
    Retrieves the URLs of papers listed on a specified webpage.

    Args:
        url (str): The URL of the webpage to scrape.
        html_list (list): A list to store the retrieved paper URLs.
        wait_time (int): Wait time in seconds before scraping.

    Returns:
        html_list (list): Updated list with URLs of papers.
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


def get_abstract_info_aea(url_paper_list, paper_number, wait_time):
    """
    Retrieves the abstract, title, authors, and issue/volume information of a paper.

    Args:
        url_paper_list (list): List of URLs to academic papers.
        paper_number (int): Index of the paper in url_paper_list to scrape.
        wait_time (int): Wait time in seconds before scraping.

    Returns:
        paper (list): A list containing paper details or an empty list in case of an error.
    """

    try:
        time.sleep(wait_time)
        service = Service(GECKO_PATH)
        browser = webdriver.Firefox(service=service)
        browser.get(url_paper_list[paper_number])
        time.sleep(wait_time)

        abstract = browser.find_element(By.CSS_SELECTOR, "section.article-information.abstract").text
        abstract = abstract.replace('Abstract', '')
        abstract = abstract.replace('\n', '')

        title = browser.find_element(By.CSS_SELECTOR, "h1.title").text

        author_elements = browser.find_elements(By.CSS_SELECTOR, "ul.attribution li.author")
        authors = ', '.join([author.text for author in author_elements])

        issue_volume_element = browser.find_element(By.CSS_SELECTOR,
                                                    "div[style='margin-top:25px;'] > div.journal:nth-of-type(2)")
        issue_volume_text = issue_volume_element.text

        # Format the text to extract volume and issue
        volume_issue = " ".join(issue_volume_text.split(",")[0:2])
        volume_issue = _reformat_volume_issue(volume_issue)

        paper = [volume_issue, [title, authors, abstract]]

    except Exception as e:
        paper = []

    browser.close()
    return paper


def _reformat_volume_issue(volume_issue):
    """
    Reformats the volume and issue string to a more standard format.

    Args:
        volume_issue (str): The original volume and issue string, e.g., 'VOL. 61 NO. 4'

    Returns:
        str: Reformatted volume and issue string, e.g., 'Volume 61, Issue 4'
    """

    # Splitting the string on spaces and removing any empty strings
    parts = [part for part in volume_issue.split() if part]

    # Finding and formatting volume and issue numbers
    volume = next((part for part in parts if part.isdigit()), None)
    issue = next((part for part in parts if part.isdigit() and part != volume), None)

    # Formatting the string
    if volume and issue:
        return f"Volume {volume}, Issue {issue}"
    elif volume:
        return f"Volume {volume}, Issue 1"
    else:
        return volume_issue
