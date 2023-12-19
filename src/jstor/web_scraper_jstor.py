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
from selenium.webdriver.firefox.service import Service as ServiceFF
from selenium.webdriver.chrome.service import Service as ServiceC
from selenium.webdriver.common.by import By
from config import GECKO_PATH, CHROME_PATH


# =============================================================================
# Functions
# =============================================================================





def get_volume_and_issue_data_jstor(url):
    service = ServiceFF(GECKO_PATH)
    browser = webdriver.Firefox(service=service)
    base_url = "https://www.jstor.org"
    browser.get(url)

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
    volume_key = f"Vol. {volume_number}"
    if volume_key in volume_dict:
        for issue in volume_dict[volume_key]:
            if issue[0] == str(issue_number):
                return issue[1]
    return "No link found for the specified volume and issue."

# 1 - Get Url from different issues
def get_papers_link_jstor(url, html_list, wait_time):
    """
    This function retrieves the URLs of papers listed on a webpage using
    Selenium and the Firefox web driver.

    Args:
        url (string): The URL of the webpage containing the list of papers.
        html_list (list): A list to store the extracted paper URLs.
        wait_time (float): The time to wait (in seconds) after loading
                           the webpage, allowing dynamic content to render before
                           extracting the links.

    Returns:
        html_list (list): A list containing the URLs of papers extracted from the webpage.
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


# 2 - Get Abstract for a specific paper


# =============================================================================
# =============================================================================
def get_abstract_info_jstor(url_paper_list, paper_number, wait_time):
    """
    This function retrieves the abstract, title, authors, and issue/volume
    information of a specific academic paper from a given list of URLs.
    It uses Selenium and the Firefox web driver to access the webpage
    containing the paper's details.

    Args:
        url_paper_list (list): A list containing URLs of academic papers' pages.
        paper_number (int): The index of the paper in url_paper_list from
                            which to retrieve the details.
        wait_time (float): The time to wait (in seconds) after loading
                           the webpage, allowing dynamic content to render before
                           extracting the details.

    Returns:
        paper (list): A list containing the issue/volume information as the
                      first element and a sublist with title, authors, and abstract as
                      the second element. If any exception occurs during scraping
                      (e.g., invalid URL, element not found), an empty list is returned.
    """
    try:
        time.sleep(wait_time)
        service = ServiceC(CHROME_PATH)
        browser = webdriver.Chrome(service=service)
        browser.get(url_paper_list[paper_number])
        time.sleep(wait_time)

        # Extract title
        print("here0")
        title = browser.find_element(By.CSS_SELECTOR,
                                     "mfe-turnaway-pharos-heading[data-pharos-component='PharosHeading']").text
        print("here1", title)
        # Extract authors
        authors = browser.find_element(By.CSS_SELECTOR, "p.content-meta-data__authors").text
        print("here2", authors)
        # Extract abstract
        abstract = browser.find_element(By.CSS_SELECTOR,
                                        "div.turnaway-preview-appendix__section--prominent p.turnaway-preview-appendix__section-paragraph").text
        print("here3", abstract)
        # Extract issue/volume information
        issue_volume = browser.find_element(By.CSS_SELECTOR,
                                            "mfe-turnaway-pharos-link[data-pharos-component='PharosLink']").text
        print("here4", issue_volume)
        paper = [issue_volume, [title, authors, abstract, "Metrics NA"]]
    except Exception as e:
        paper = []



    browser.close()
    return paper
