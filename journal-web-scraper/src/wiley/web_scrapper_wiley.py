# -*- coding: utf-8 -*-

"""
Web Scraper for Academic Journals - Wiley Module

This module provides a web scraping tool to extract data from academic journals published by Wiley.
It automates the process of accessing journal webpages and collecting information such as article titles,
authors, abstracts, and issue/volume details using Python, Selenium, and the Firefox web driver.
The tool is designed to assist in gathering data for academic research and analysis.

Functions:
    get_latest_volume_number_wiley(url, wait_time): Retrieves the latest volume number from a specified Wiley journal.
    get_paper_number_from_name_wiley(name): Retrieves the internal paper number associated with a Wiley journal name.
    get_num_issues_wiley(name): Retrieves the number of issues available for a specified Wiley journal.
    get_papers_link_wiley(url, html_list, wait_time): Retrieves URLs of papers from a specified Wiley journal webpage.
    get_abstract_info_wiley(url_paper_list, paper_number, wait_time): Extracts detailed information from a Wiley paper's webpage,
        including abstract, title, authors, and issue/volume information.

Usage:
    1. Retrieve paper number from journal name:
        paper_number = get_paper_number_from_name_wiley(journal_name)

    2. Retrieve the latest volume number:
        latest_volume_number = get_latest_volume_number_wiley(journal_url, wait_time)

    3. Retrieve the number of issues:
        num_issues = get_num_issues_wiley(journal_name)

    4. Collect paper URLs:
        paper_urls = get_papers_link_wiley(journal_url, [], wait_time)

    5. Extract paper details:
        paper_info = get_abstract_info_wiley(paper_urls, paper_index, wait_time)
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
from src.helperFunctions.generateKey import generate_key

# =============================================================================
# Functions
# =============================================================================


def get_paper_number_from_name_wiley(name):
    """
    Retrieves the internal paper number associated with a Wiley journal name.

    Args:
        name (str): The name of the Wiley journal.

    Returns:
        int: The internal paper number for the specified journal, if found.
        None: If the journal name is not in the dictionary or an error occurs.
    """

    try:
        with open('wiley_journal_name_to_int_and_num_issues.json', 'r') as file:
            name_dict = json.load(file)
    except:
        with open('wiley/wiley_journal_name_to_int_and_num_issues.json', 'r') as file:
            name_dict = json.load(file)

    try:
        return name_dict[name][0]
    except KeyError:
        print(
            f"The journal name: {name} either is not a Wiley journal or has not been added to name->int/#issues dict.")


def get_num_issues_wiley(name):
    """
    Retrieves the number of issues for a specified Wiley journal.

    Args:
        name (str): The name of the Wiley journal.

    Returns:
        int: The number of issues for the specified journal, if found.
        None: If the journal name is not in the dictionary or an error occurs.
    """

    try:
        with open('wiley_journal_name_to_int_and_num_issues.json', 'r') as file:
            name_dict = json.load(file)
    except:
        with open('wiley/wiley_journal_name_to_int_and_num_issues.json', 'r') as file:
            name_dict = json.load(file)

    try:
        return name_dict[name][1]
    except KeyError:
        print(
            f"The journal name: {name} either is not a Wiley journal or has not been added to name->int/#issues dict.")


def get_latest_volume_number_wiley(url, wait_time):
    """
    Retrieves the latest volume number from the specified Wiley journal webpage.

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
        volume_element = browser.find_element(By.CSS_SELECTOR, "div.cover-image__details span.comma")
        volume_text = volume_element.text
        match = re.search(r"Volume (\d+)", volume_text)
        if match:
            volume_number = int(match.group(1))

    except Exception as e:
        print("Error: " + str(e))

    finally:
        browser.close()

    return volume_number


def get_papers_link_wiley(url, html_list, wait_time):
    """
    Retrieves URLs of papers from a specified Wiley journal webpage.

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
    articles = browser.find_elements(By.XPATH, "//a[contains(@class, 'issue-item__title visitable')]")

    # Construct the full URL for each paper and add it to the list
    base_url = "https://onlinelibrary.wiley.com"

    for article in articles:
        partial_link = article.get_attribute('href')
        full_link = base_url + partial_link if partial_link.startswith("/doi") else partial_link
        html_list.append(full_link)

    # Close the browser
    browser.close()

    return html_list


def get_abstract_info_wiley(url_paper_list, paper_number, wait_time, journal_name):
    """
    Retrieves detailed information of a specific paper from Wiley.

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

        WebDriverWait(browser, wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, "volume-issue"))
        )

        # Find the volume-issue element and extract text
        volume_issue_element = browser.find_element(By.CLASS_NAME, 'volume-issue')
        volume_issue_text = volume_issue_element.get_attribute('outerHTML')
        match = re.search(r"Volume (\d+), Issue (\d+)", volume_issue_text)
        if match:
            volume = match.group(1)
            issue = match.group(2)
            issue_volume = f"Volume {volume}, Issue {issue}"
        else:
            issue_volume = "Volume/Issue info not found"

        # Find the citation title
        citation_title = browser.find_element(By.CLASS_NAME, 'citation__title').text

        authors_elements = browser.find_elements(By.XPATH,
                                                 "//div[@id='sb-1']/div/div/span/a/span")
        authors = ", ".join([author.text for author in authors_elements])

        abstract = browser.find_element(By.XPATH, "//div[contains(@class, 'article-section__content')]/p").text

        # key = generate_key('Wiley', journal_name, issue_volume.split(" ")[1].replace(',', ''), issue_volume.split(" ")[-1])
        # paper = [key, issue_volume, [citation_title, authors, abstract]]

        paper = [issue_volume, [citation_title, authors, abstract]]

    except Exception as e:
        paper = []

    finally:
        browser.close()

    return paper
