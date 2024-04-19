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
import json
from src.helperFunctions.generateKey import generate_key



# =============================================================================
# Functions
# =============================================================================


def get_num_issues_uchicago(name):
    try:
        with open('uchicago_journal_name_to_num_issues_and_full_name.json', 'r') as file:
            name_dict = json.load(file)
    except:
        with open('uchicago/uchicago_journal_name_to_num_issues_and_full_name.json', 'r') as file:
            name_dict = json.load(file)

    try:
        return name_dict[name][0]
    except KeyError:
        print(f"The journal name: {name} either is not a UChicago journal or has not been added to name->#issues dict, fullname.")

def get_full_name_uchicago(name):
    try:
        with open('uchicago_journal_name_to_num_issues_and_full_name.json', 'r') as file:
            name_dict = json.load(file)
    except:
        with open('uchicago/uchicago_journal_name_to_num_issues_and_full_name.json', 'r') as file:
            name_dict = json.load(file)

    try:
        return name_dict[name][1]
    except KeyError:
        print(
            f"The journal name: {name} either is not a UChicago journal or has not been added to name->#issues dict.")


def get_latest_volume_uchicago(journal_name):
    service = Service(GECKO_PATH)
    browser = webdriver.Firefox(service=service)
    journal_url = f'https://www.journals.uchicago.edu/toc/{journal_name}/current'
    browser.get(journal_url)

    time.sleep(5)  # Wait for the page to load

    try:
        # Locate the elements containing volume and issue information
        volume_element = browser.find_element(By.CSS_SELECTOR, "div.cover-image__details .journal-meta span.citation-line:first-child")

        volume_info = volume_element.text

        volume_match = re.search(r"Volume (\d+)", volume_info)
        if volume_match:
            latest_volume = int(volume_match.group(1))
        else:
            raise ValueError("Volume or issue number not found")

    except Exception as e:
        print(f"Error occurred: {e}")
        latest_volume = None

    finally:
        browser.close()

    return latest_volume

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


def get_abstract_info_uchicago(url_paper_list, paper_number, wait_time, journal_name):
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

        # key = generate_key('UChicago', journal_name, issue_volume.split(" ")[1].replace(',', ''), issue_volume.split(" ")[-1])
        # paper = [key, issue_volume, [title, authors, abstract]]
        paper = [issue_volume, [title, authors, abstract]]
    except Exception as e:
        paper = []

    finally:
        browser.close()
    return paper

