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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =============================================================================
# Functions
# =============================================================================


def get_volume_and_issue_data_uchicago(journal_name):
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

# 1 - Get Url from different issues
def get_papers_link_uchicago(url, html_list, wait_time):
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
    browser = webdriver.Firefox(service=service)
    browser.get(url)
    time.sleep(wait_time)
    # Updated selector for DOI links
    links = browser.find_elements(By.CSS_SELECTOR, "div.issue-item h4.issue-item__title a")
    for link in links:
        html_list.append(link.get_attribute('href'))

    browser.close()
    return html_list


# 2 - Get Abstract for a specific paper
def get_abstract_info_uchicago(url_paper_list, paper_number, wait_time):
    """
    Retrieves abstract, title, authors, and issue/volume information for an academic paper.

    Args:
        url_paper_list (list): URLs of academic papers.
        paper_number (int): Index of the paper in url_paper_list.
        wait_time (float): Time to wait for dynamic content to load.

    Returns:
        paper (list): [issue/volume, [title, authors, abstract]].
    """
    try:
        service = Service(GECKO_PATH)
        browser = webdriver.Firefox(service=service)
        browser.get(url_paper_list[paper_number])
        time.sleep(wait_time)

        print("here0")
        title = browser.find_element(By.CSS_SELECTOR, "h1.citation__title").text
        print("here1")
        authors = ', '.join([author.text for author in browser.find_elements(By.CSS_SELECTOR, "a.author-name span")])
        print("here2")
        abstract = browser.find_element(By.CSS_SELECTOR, "div.abstractSection.abstractInFull p").text
        print("here3")
        issue_volume = browser.find_element(By.CSS_SELECTOR, ".current-issue__meta").text
        print("here4")

        paper = [issue_volume, [title, authors, abstract, 'Metrics NA']]
    except Exception as e:
        paper = []

    browser.close()
    return paper
