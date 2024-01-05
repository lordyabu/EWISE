# -*- coding: utf-8 -*-

# Currently not in use ///////////////////////////////////

"""
Web Scraper for Academic Journals - JSTOR Module

This module provides a web scraping tool to extract data from academic journals available on JSTOR.
It uses Python programming language and the Selenium library, along with Firefox and Chrome web drivers,
to automate the process of accessing academic journal webpages and collecting relevant information like
article titles, authors, abstracts, and other details. The tool is tailored for research purposes, enabling
efficient data collection from JSTOR.

Functions:
    get_volume_and_issue_data_jstor(url): Retrieves volume and issue data from a specified JSTOR journal.
    get_link_from_dict_jstor(volume_dict, volume_number, issue_number): Gets the link for a specific volume and issue from the volume dictionary.
    get_papers_link_jstor(url, html_list, wait_time): Collects URLs of papers from a JSTOR journal's webpage.
    get_abstract_info_jstor(url_paper_list, paper_number, wait_time): Extracts detailed information from a paper's webpage on JSTOR.

Usage:
    1. Retrieve volume and issue data:
        volume_issue_data = get_volume_and_issue_data_jstor(journal_url)

    2. Get a specific link for a volume and issue:
        specific_link = get_link_from_dict_jstor(volume_issue_data, volume_number, issue_number)

    3. Collect paper URLs:
        paper_urls = get_papers_link_jstor(specific_link, [], wait_time)

    4. Extract paper details:
        paper_info = get_abstract_info_jstor(paper_urls, paper_index, wait_time)
"""

# =============================================================================
# Packages
# =============================================================================
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as ServiceFF
from selenium.webdriver.chrome.service import Service as ServiceC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import GECKO_PATH, CHROME_PATH


# =============================================================================
# Functions
# =============================================================================
def get_volume_and_issue_data_jstor(url, wait_time):
    """
    Retrieves volume and issue data from the specified JSTOR journal URL.

    Args:
        url (str): URL of the JSTOR journal page to scrape.

    Returns:
        volume_dict (dict): A dictionary mapping each volume to its issues and corresponding URLs.
    """

    def click_dropdowns():
        details_elements = browser.find_elements(By.CLASS_NAME, "decade")

        for detail in details_elements:
            # Scroll the detail element into view
            browser.execute_script("arguments[0].scrollIntoView(true);", detail)
            time.sleep(1)  # Short wait after scrolling

            try:
                # Try clicking the element
                if not detail.get_attribute('open'):
                    detail.click()
                    time.sleep(wait_time)  # Wait for content to load
            except Exception:
                # If click fails, use JavaScript to forcibly click the element
                browser.execute_script("arguments[0].click();", detail)


    service = ServiceC(CHROME_PATH)
    browser = webdriver.Chrome(service=service)
    base_url = "https://www.jstor.org"
    browser.get(url)

    time.sleep(wait_time)

    click_dropdowns()

    time.sleep(wait_time)

    # Dictionary to store volume: [(issue_number, link)]
    volume_dict = {}

    # Find all decade sections
    decade_elements = browser.find_elements(By.CLASS_NAME, "decade")
    for decade in decade_elements:
        # Find all volume elements within this decade
        volume_elements = decade.find_elements(By.CLASS_NAME, "year-volume-heading")

        for volume_element in volume_elements:
            volume_strong = volume_element.find_element(By.TAG_NAME, "strong")
            volume = volume_strong.text.split('(')[1].split(')')[
                0] if '(' in volume_strong.text else volume_strong.text  # Extract volume number

            issue_elements = volume_element.find_elements(By.TAG_NAME, "li")

            issue_list = []
            issue_num = len(issue_elements)  # Start with the number of issues as the highest issue number
            for issue in issue_elements:
                # Extracting the link
                link_element = issue.find_element(By.TAG_NAME, "collection-view-pharos-link")
                link = link_element.get_attribute('href')
                if not link.startswith('http'):
                    link = base_url + link  # Construct the full URL if it's a relative link

                issue_list.append((str(issue_num), link))
                issue_num -= 1  # Decrease the issue number for the next issue

            volume_dict[volume] = issue_list

    # browser.close()
    return volume_dict


def get_link_from_dict_jstor(volume_dict, volume_number, issue_number):
    """
    Retrieves the link for a specific volume and issue from a volume dictionary.

    Args:
        volume_dict (dict): A dictionary containing volume and issue data.
        volume_number (int): The volume number.
        issue_number (int): The issue number within the volume.

    Returns:
        str: URL link for the specified volume and issue, or a message if not found.
    """
    volume_key = f"Vol. {volume_number}"
    if volume_key in volume_dict:
        for issue in volume_dict[volume_key]:
            if issue[0] == str(issue_number):
                return issue[1]
    return "No link found for the specified volume and issue."


def get_papers_link_jstor(url, html_list, wait_time):
    """
    Retrieves URLs of papers from a specified JSTOR journal webpage.

    Args:
        url (str): URL of the journal's webpage.
        html_list (list): List to store the paper URLs.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        html_list (list): Updated list with URLs of papers.
    """
    time.sleep(wait_time)
    service = ServiceC(CHROME_PATH)
    browser = webdriver.Chrome(service=service)
    browser.get(url)
    time.sleep(wait_time)

    # Find all <div> elements with class 'stable' which contains the paper links
    links = browser.find_elements(By.CSS_SELECTOR, "div.stable")

    for link in links:
        paper_url = link.text  # Extract the URL text from the <div> element
        if paper_url.startswith("http"):  # Ensure it's a valid URL
            html_list.append(paper_url)

    browser.close()
    return html_list


def get_abstract_info_jstor(url_paper_list, paper_number, wait_time):
    """
    Retrieves detailed information of a specific paper from JSTOR.

    Args:
        url_paper_list (list): List of paper URLs.
        paper_number (int): Index of the paper in the list.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        paper (list): A list containing detailed information of the paper.
    """
    try:
        time.sleep(wait_time)
        service = ServiceC(CHROME_PATH)
        browser = webdriver.Chrome(service=service)
        browser.get(url_paper_list[paper_number])
        time.sleep(wait_time)
        title = browser.find_element(By.CSS_SELECTOR,
                                     "mfe-turnaway-pharos-heading[data-pharos-component='PharosHeading']").text
        authors = browser.find_element(By.CSS_SELECTOR, "p.content-meta-data__authors").text
        abstract = browser.find_element(By.CSS_SELECTOR,
                                        "div.turnaway-preview-appendix__section--prominent p.turnaway-preview-appendix__section-paragraph").text
        issue_volume = browser.find_element(By.CSS_SELECTOR,
                                            "mfe-turnaway-pharos-link[data-pharos-component='PharosLink']").text
        paper = [issue_volume, [title, authors, abstract]]
    except Exception as e:
        paper = []

    browser.close()
    return paper
