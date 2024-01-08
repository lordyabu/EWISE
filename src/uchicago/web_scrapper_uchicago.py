# -*- coding: utf-8 -*-

"""
Web Scraper for Academic Journals - University of Chicago Module

This module provides a web scraping tool to extract data from academic journals published by the University of Chicago.
It uses Python, Selenium, and the Firefox web driver to automate the process of accessing academic journal webpages
and collecting relevant information, including article titles, authors, abstracts, and other details. The tool is
particularly designed to scrape data from the University of Chicago's journal webpages.

Functions:
    get_volume_and_issue_data_uchicago(journal_name): Retrieves volume and issue data for a specified University of Chicago journal.
    get_papers_link_uchicago(url, html_list, wait_time): Scrapes URLs of papers listed on a journal's webpage.
    get_abstract_info_uchicago(url_paper_list, paper_number, wait_time): Extracts abstract, title, authors,
        and issue/volume information from a paper's webpage.

Usage:
    1. Collect paper URLs:
        paper_urls = get_papers_link_uchicago(journal_url, [], wait_time)

    2. Extract paper details:
        paper_info = get_abstract_info_uchicago(paper_urls, paper_index, wait_time)
"""

# =============================================================================
# Packages
# =============================================================================
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from config import GECKO_PATH
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


# =============================================================================
# Functions
# =============================================================================

# Currently Not in use
def get_volume_and_issue_data_uchicago(journal_name):
    """
    Retrieves volume and issue data from the specified University of Chicago journal URL.

    Args:
        journal_name (str): Name of the University of Chicago journal.

    Returns:
        volume_dict (dict): A dictionary mapping each volume to its issues and corresponding URLs.
    """
    service = Service(GECKO_PATH)
    browser = webdriver.Firefox(service=service)
    journal_url = f'https://www.journals.uchicago.edu/loi/{journal_name}'
    browser.get(journal_url)

    # Dictionary to store volume: [(issue_number, link)]
    volume_dict = {}

    # Wait for the page to load
    wait = WebDriverWait(browser, 10)
    accordion_triggers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "js-accordion__trigger")))

    # Iterate over each accordion trigger to open it
    for trigger in accordion_triggers:
        browser.execute_script("arguments[0].click();", trigger)

        # Wait for the content to load
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "loi-volume__issue-dot")))

        # Now find all issue link elements within the opened section
        issue_link_elements = browser.find_elements(By.CLASS_NAME, "loi-volume__issue-dot")

        for issue_link_element in issue_link_elements:
            link = issue_link_element.get_attribute('href')
            full_link = link if link.startswith('http') else 'https://www.journals.uchicago.edu' + link

            volume_text_element = issue_link_element.find_element(By.CLASS_NAME, "issue__vol")
            issue_text_element = issue_link_element.find_element(By.CLASS_NAME, "issue__issue")

            volume = volume_text_element.text.replace("Volume ", "").strip()
            issue_number = issue_text_element.text.replace("Number ", "").strip()

            if volume not in volume_dict:
                volume_dict[volume] = []
            volume_dict[volume].append((issue_number, full_link))

    browser.close()
    return volume_dict


def get_papers_link_uchicago(url, html_list, wait_time):
    """
    Retrieves URLs of papers from a specified University of Chicago journal webpage.

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

    # Updated selector for DOI links
    links = browser.find_elements(By.CSS_SELECTOR, "div.issue-item h4.issue-item__title a")
    for link in links:
        html_list.append(link.get_attribute('href'))

    browser.close()
    return html_list


def get_abstract_info_uchicago(url_paper_list, paper_number, wait_time):
    """
    Retrieves detailed information of a specific paper from the University of Chicago.

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
        title = browser.find_element(By.CSS_SELECTOR, "h1.citation__title").text
        authors = ', '.join([author.text for author in browser.find_elements(By.CSS_SELECTOR, "a.author-name span")])
        abstract = browser.find_element(By.CSS_SELECTOR, "div.abstractSection.abstractInFull p").text


        issue_volume_text = browser.find_element(By.CSS_SELECTOR, ".current-issue__meta").text
        volume_issue_match = re.search(r'Volume (\d+), Number (\d+)', issue_volume_text)
        if volume_issue_match:
            volume = volume_issue_match.group(1)
            issue = volume_issue_match.group(2)
            issue_volume = f"Volume {volume}, Issue {issue}"
        else:
            # Fallback in case the regex doesn't find a match
            issue_volume = "Volume and issue information not found"

        paper = [issue_volume, [title, authors, abstract]]
    except Exception as e:
        paper = []

    browser.close()
    return paper
