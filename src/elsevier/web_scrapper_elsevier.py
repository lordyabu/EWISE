# -*- coding: utf-8 -*-

"""
Web Scraper for Academic Journals - Elsevier Module

This module provides a web scraping tool to extract data from academic journals published by Elsevier.
It automates the process of accessing journal webpages and collecting information such as article titles,
authors, abstracts, and issue/volume details using Python, Selenium, and the Firefox web driver.
The tool is designed to assist in gathering data for academic research and analysis.

Functions:
    get_volume_and_issue_data_elsevier(journal_name): Retrieves volume and issue data for a specified Elsevier journal.
    get_papers_link_elsevier(url, html_list, wait_time): Retrieves URLs of papers from a specified Elsevier journal webpage.
    get_abstract_info_elsevier(url_paper_list, paper_number, wait_time): Extracts detailed information from a paper's webpage,
        including abstract, title, authors, and issue/volume information.

Usage:
    1. Collect paper URLs:
        paper_urls = get_papers_link_elsevier(journal_url, [], wait_time)

    2. Extract paper details:
        paper_info = get_abstract_info_elsevier(paper_urls, paper_index, wait_time)
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


# =============================================================================
# Functions
# =============================================================================


# Currently Not in use
def get_volume_and_issue_data_elsevier(journal_name):
    """
    Retrieves volume and issue data from the specified Elsevier journal URL.

    Args:
        journal_name (str): Name of the Elsevier journal.

    Returns:
        volume_dict (dict): A dictionary mapping each volume to its issues and corresponding URLs.
    """
    service = Service(GECKO_PATH)
    browser = webdriver.Firefox(service=service)
    journal_url = f'https://www.sciencedirect.com/journal/{journal_name}/issues'
    time.sleep(5)
    browser.get(journal_url)

    # Dictionary to store volume: [link]
    volume_dict = {}

    # Find all issue link elements
    issue_link_elements = browser.find_elements(By.CLASS_NAME, "js-issue-item-link")
    for issue_link_element in issue_link_elements:
        link = issue_link_element.get_attribute('href')
        full_link = link if link.startswith('http') else 'https://www.sciencedirect.com' + link

        volume_text = issue_link_element.text
        volume_match = re.search(r"Volume (\d+)", volume_text)
        if volume_match:
            volume = volume_match.group(1)
            if volume not in volume_dict:
                volume_dict[volume] = []
            volume_dict[volume].append(full_link)

    browser.close()
    return volume_dict


def get_papers_link_elsevier(url, html_list, wait_time):
    """
    Retrieves URLs of papers from a specified Elsevier journal webpage.

    Args:
        url (str): URL of the journal's webpage.
        html_list (list): List to store the paper URLs.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        html_list (list): Updated list with URLs of papers.
    """
    service = Service(GECKO_PATH)
    browser = webdriver.Firefox(service=service)
    browser.get(url)
    time.sleep(wait_time)
    links = browser.find_elements(By.XPATH, "//h3/a")
    for i in links:
        html_list.append(i.get_attribute('href'))
    browser.close()
    return html_list


def get_abstract_info_elsevier(url_paper_list, paper_number, wait_time):
    """
    Retrieves detailed information of a specific paper from Elsevier.

    Args:
        url_paper_list (list): List of paper URLs.
        paper_number (int): Index of the paper in the list.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        paper (list): A list containing detailed information of the paper.
    """
    try:
        service = Service(GECKO_PATH)
        browser = webdriver.Firefox(service=service)
        browser.get(url_paper_list[paper_number])
        time.sleep(wait_time)
        abstract = browser.find_element(By.ID, 'abstracts').text
        title = browser.find_element(By.ID, 'screen-reader-main-title').text
        authors = browser.find_element(By.ID, 'author-group').text
        issue_volume = browser.find_element(By.ID, 'publication-title').text
        paper = [issue_volume, [title, authors, abstract]]
    except Exception as e:
        paper = []

    browser.close()
    return paper
