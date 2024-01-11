# -*- coding: utf-8 -*-

"""
Web Scraper for Academic Journals - springer Module

This module provides a web scraping tool to extract data from academic journals published by springer.
It automates the process of accessing journal webpages and collecting information such as article titles,
authors, abstracts, and issue/volume details using Python, Selenium, and the Firefox web driver.
The tool is designed to assist in gathering data for academic research and analysis.

Functions:
    get_papers_link_springer(url, html_list, wait_time): Retrieves URLs of papers from a specified springer journal webpage.
    get_abstract_info_springer(url_paper_list, paper_number, wait_time): Extracts detailed information from a springer paper's webpage,
        including abstract, title, authors, and issue/volume information.

Usage:
    1. Collect paper URLs:
        paper_urls = get_papers_link_springer(journal_url, [], wait_time)

    2. Extract paper details:
        paper_info = get_abstract_info_springer(paper_urls, paper_index, wait_time)
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




# =============================================================================
# Functions
# =============================================================================


#DONE
def get_latest_volume_number_springer(url, wait_time):
    """
    Retrieves the latest volume number from the specified Springer journal webpage.

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

        # Find the first occurrence of the volume element and extract the number
        try:
            # Try the first CSS selector
            volume_element = browser.find_element(By.CSS_SELECTOR, "li.app-section h2.app-section__heading span.u-display-block.u-flex-grow")
        except:
            # If the first selector fails, try the second one
            volume_element = browser.find_element(By.CSS_SELECTOR, "li.app-vol-and-issues-item h2 span")
        volume_text = volume_element.text
        match = re.search(r"Volume (\d+)", volume_text)
        if match:
            volume_number = int(match.group(1))

    except Exception as e:
        print("Error: " + str(e))

    finally:
        browser.close()

    return volume_number


#DONE
def get_paper_number_from_name_springer(name):
    try:
        with open('springer_journal_name_to_int_and_num_issues.json', 'r') as file:
            name_dict = json.load(file)
    except:
        with open('springer/springer_journal_name_to_int_and_num_issues.json', 'r') as file:
            name_dict = json.load(file)

    try:
        return name_dict[name][0]
    except KeyError:
        print(f"The journal name: {name} either is not a springer journal or has not been added to name->int/#issues dict.")


#DONE
def get_num_issues_springer(name):
    try:
        with open('springer_journal_name_to_int_and_num_issues.json', 'r') as file:
            name_dict = json.load(file)
    except:
        with open('springer/springer_journal_name_to_int_and_num_issues.json', 'r') as file:
            name_dict = json.load(file)

    try:
        return name_dict[name][1]
    except KeyError:
        print(f"The journal name: {name} either is not a springer journal or has not been added to name->int/#issues dict.")


#DONE
def get_papers_link_springer(url, html_list, wait_time):
    """
    Retrieves URLs of papers from a specified Springer journal webpage.

    Args:
        url (str): URL of the journal's webpage.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        paper_links (list): List of URLs of papers.
    """
    try:
        service = Service(GECKO_PATH)
        browser = webdriver.Firefox(service=service)
        browser.get(url)

        # Wait for the page to render
        time.sleep(wait_time)

        # Find all elements that match the desired selector
        articles = browser.find_elements(By.CSS_SELECTOR, "article.c-card-open h3.c-card-open__heading a")

        # IMF for some reason does not follow above format here
        if not articles:
            articles = browser.find_elements(By.CSS_SELECTOR, "li.c-list-group__item a")

        for article in articles:
            link = article.get_attribute('href')
            html_list.append(link)

    except Exception as e:
        print("Error: " + str(e))

    finally:
        browser.close()

    return html_list

#DONE
def get_abstract_info_springer(url_paper_list, paper_number, wait_time):
    """
    Retrieves detailed information of a specific paper from Springer.

    Args:
        url_paper_list (list): List of paper URLs.
        paper_number (int): Index of the paper in the list.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        paper (list): A list containing detailed information of the paper.
    """
    paper = []
    try:
        service = Service(GECKO_PATH)
        browser = webdriver.Firefox(service=service)
        browser.get(url_paper_list[paper_number])

        WebDriverWait(browser, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.c-article-title"))
        )

        # Find the title
        title = browser.find_element(By.CSS_SELECTOR, 'h1.c-article-title').text

        # Find the authors
        authors_elements = browser.find_elements(By.CSS_SELECTOR, "ul.c-article-author-list li a[data-test='author-name']")
        authors = ", ".join([author.text for author in authors_elements])

        # Find the abstract
        abstract = browser.find_element(By.CSS_SELECTOR, 'div.c-article-section__content p').text

        # Find the volume and set issue to 'X'
        volume_element = browser.find_element(By.CSS_SELECTOR, 'span[data-test="journal-volume"]')
        volume = volume_element.text.replace("Volume", "").strip()
        issue = "X"  # Page does not show issue

        paper = [f"Volume {volume}, Issue {issue}", title, authors, abstract]
    except Exception as e:
        print("Error: " + str(e))

    finally:
        browser.close()

    return paper


