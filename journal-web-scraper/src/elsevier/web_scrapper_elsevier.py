# -*- coding: utf-8 -*-

"""
Web Scraper for Academic Journals - Elsevier Module

This module provides a web scraping tool to extract data from academic journals published by Elsevier.
It automates the process of accessing journal webpages and collecting information such as article titles,
authors, abstracts, and issue/volume details using Python, Selenium, and the Firefox web driver.
The tool is designed to assist in gathering data for academic research and analysis.

Functions:
    get_num_issues_elsevier(journal_name): Retrieves the number of issues available for a specified Elsevier journal.
    get_latest_volume_elsevier(journal_name): Retrieves the latest volume for a specified Elsevier journal.
    get_papers_link_elsevier(url, html_list, wait_time): Retrieves URLs of papers from a specified Elsevier journal webpage.
    get_abstract_info_elsevier(url_paper_list, paper_number, wait_time): Extracts detailed information from an Elsevier paper's webpage,
        including abstract, title, authors, and issue/volume information.

Usage:
    1. Retrieve the latest volume number:
        latest_volume_number = get_latest_volume_elsevier(journal_url, wait_time)

    2. Retrieve the number of issues:
        num_issues = get_num_issues_elsevier(journal_name)

    3. Collect paper URLs:
        paper_urls = get_papers_link_elsevier(journal_url, [], wait_time)

    4. Extract paper details:
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
import json
from src.helperFunctions.generateKey import generate_key


# =============================================================================
# Functions
# =============================================================================


def convert_elsevier_name(journal):
    new = ""
    for i in journal.split("-"):
        if i == "of" or i == "and" or i == "to":
            new = new + i + " "
        else:
            new = new + i.capitalize() + " "
    return new

def get_num_issues_elsevier(name):
    """
    Retrieves the number of issues available for a specified Elsevier journal.

    Args:
        name (str): Name of the Elsevier journal.

    Returns:
        int or str: Number of issues if available, else 'No Issues'.
    """

    try:
        with open('elsevier_journals_with_issues.json', 'r') as file:
            name_dict = json.load(file)
    except:
        with open('elsevier/elsevier_journals_with_issues.json', 'r') as file:
            name_dict = json.load(file)

    try:
        return name_dict[name]
    except KeyError:
        return "No Issues"


def get_latest_volume_elsevier(journal_name):
    """
    Retrieves the latest volume number of a specified Elsevier journal.

    Args:
        journal_name (str): The name of the Elsevier journal.

    Returns:
        str: The latest volume number, or None if not found.
    """

    service = Service(GECKO_PATH)
    browser = webdriver.Firefox(service=service)
    journal_url = f'https://www.sciencedirect.com/journal/{journal_name}/issues'
    time.sleep(5)
    browser.get(journal_url)

    # Find all issue link elements
    issue_link_elements = browser.find_elements(By.CLASS_NAME, "js-issue-item-link")
    for issue_link_element in issue_link_elements:
        volume_text = issue_link_element.text
        volume_match = re.search(r"Volume (\d+)", volume_text)
        if volume_match:
            volume = volume_match.group(1)
            browser.close()
            return volume

    browser.close()


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


def get_abstract_info_elsevier(url_paper_list, paper_number, wait_time, journal_name):
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
        abstract = abstract.replace('Highlights\n', '')
        abstract = abstract.replace('Abstract ', '')
        abstract = abstract.replace('\n', ' ')
        abstract = abstract.replace('•', '')

        title = browser.find_element(By.ID, 'screen-reader-main-title').text
        title = re.sub(r'[^A-Za-z0-9 ]+', '', title)

        authors = browser.find_element(By.ID, 'author-group').text
        authors = authors.replace('Author links open overlay panel', '')
        authors = authors.replace('\n', '')
        authors = re.sub(r'\s*\d+\s*', '', authors)

        # Locate the element that contains the volume and issue information
        volume_issue_info = browser.find_element(By.CSS_SELECTOR, ".publication-volume .text-xs")
        volume_issue_text = volume_issue_info.text.split(",")[0:2]

        # Check if the second part starts with 'I' (indicating 'Issue')
        if len(volume_issue_text) > 1 and volume_issue_text[1].strip().startswith('I'):
            volume_issue = " ".join(volume_issue_text)
        else:
            volume_issue = volume_issue_text[0] + ", Issue 1"

        # key = generate_key('Elsevier', journal_name, volume_issue.split(" ")[1].replace(',', ''), volume_issue.split(" ")[-1])
        # paper = [key, volume_issue, [title, authors, abstract]]
        paper = [volume_issue, [title, authors, abstract]]

    except Exception as e:

        paper = []
    finally:
        browser.close()
    return paper
