# -*- coding: utf-8 -*-
"""
Web Scraper for Academic Journals - Oxford Module

This module provides a web scraping tool to extract data from academic journals published by Oxford.
It automates the process of accessing journal webpages and collecting information such as article titles,
authors, abstracts, and issue/volume details using Python, Selenium, and the Firefox web driver.
The tool is designed to assist in gathering data for academic research and analysis.

Functions:
    get_latest_volume_number_oxford(url, wait_time): Retrieves the latest volume number from a specified Oxford journal.
    get_num_issues_oxford(name): Retrieves the number of issues available for a specified Oxford journal.
    get_papers_link_oxford(url, html_list, wait_time): Retrieves URLs of papers from a specified Oxford journal webpage.
    get_abstract_info_oxford(url_paper_list, paper_number, wait_time): Extracts detailed information from an Oxford paper's webpage,
        including abstract, title, authors, and issue/volume information.

Usage:
    1. Retrieve the latest volume number:
        latest_volume_number = get_latest_volume_number_oxford(journal_url, wait_time)

    2. Retrieve the number of issues:
        num_issues = get_num_issues_oxford(journal_name)

    3. Collect paper URLs:
        paper_urls = get_papers_link_oxford(journal_url, [], wait_time)

    4. Extract paper details:
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


# =============================================================================
# Functions
# =============================================================================


def get_num_issues_oxford(name):
    """
    Retrieves the number of issues for a specified Oxford journal.

    Args:
        name (str): The name of the Oxford journal.

    Returns:
        int or None: The number of issues if the journal is found, otherwise None.
    """

    try:
        with open('oxford_name_to_num_issues.json', 'r') as file:
            name_dict = json.load(file)
    except:
        with open('oxford/oxford_name_to_num_issues.json', 'r') as file:
            name_dict = json.load(file)

    try:
        return name_dict[name]
    except KeyError:
        print(f"The journal name: {name} either is not an Oxford journal or has not been added to name->num_issue dict.")


def get_latest_volume_number_oxford(url, wait_time):
    """
    Retrieves the latest volume number from the specified webpage.

    Args:
        url (str): URL of the journal's webpage.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        int: The latest volume number as an integer.
    """

    volume_number = 0
    try:
        service = Service(GECKO_PATH)
        browser = webdriver.Firefox(service=service)
        browser.get(url)

        # Wait for the page to render
        time.sleep(wait_time)

        # Find the volume element and extract the number
        volume_element = browser.find_element(By.CSS_SELECTOR, "span.volume")
        volume_text = volume_element.text
        match = re.search(r"Volume (\d+)", volume_text)
        if match:
            volume_number = int(match.group(1))

    except Exception as e:
        print("Error: " + str(e))

    finally:
        browser.close()

    return volume_number


def get_papers_link_oxford(url, html_list, wait_time):
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

    # Construct the full URL for each paper and add it to the list
    base_url = "https://academic.oup.com"

    for article in articles:
        partial_link = article.get_attribute('href')
        full_link = base_url + partial_link if partial_link.startswith("/doi") else partial_link
        html_list.append(full_link)

    # Close the browser
    browser.close()

    return html_list


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
        abstract = browser.find_element(By.CSS_SELECTOR, "section.abstract p").text
        abstract = re.sub(r'\\u\d{4}', '', abstract)

        # Find the volume and issue
        volume = browser.find_element(By.CSS_SELECTOR, "div.volume-issue__wrap .volume").text
        issue = browser.find_element(By.CSS_SELECTOR, "div.volume-issue__wrap .issue").text
        issue_volume = f"{volume}, {issue}"

        paper = [issue_volume, [title, authors, abstract]]
    except Exception as e:
        paper = []

    finally:
        browser.close()

    return paper

