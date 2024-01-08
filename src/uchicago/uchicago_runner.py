# -*- coding: utf-8 -*-

# =============================================================================
# UChicago Journal Web Scraper
# =============================================================================
"""
This module provides a tool for web scraping academic journals published by the University of Chicago.
It extracts article titles, authors, abstracts, and issue/volume information using Python, Selenium,
and the Firefox web driver. The data is collected from journal webpages and saved in JSON format.

Functions:
    scrape_uchicago_journal(journal_name, volumes, issues): Scrapes articles from a specified
        University of Chicago journal.
    scrape_multiple_uchicago_journals(journal_list, volumes, issues): Scrapes multiple journals
        based on the provided list of journal names.

Usage:
    To scrape a single journal:
        scrape_uchicago_journal('journal-name', [volume_numbers], [issue_numbers])

    To scrape multiple journals:
        journal_list = ['journal1', 'journal2', ...]
        scrape_multiple_uchicago_journals(journal_list, [volume_numbers], [issue_numbers])
"""

# =============================================================================
# Packages
# =============================================================================

# General Modules
import os.path
import sys
import json
from tqdm import tqdm
from config import USER_PATH, DATA_PATH

# Developed Modules
sys.path.append(os.path.join(USER_PATH, 'src'))
from src.uchicago.web_scrapper_uchicago import get_papers_link_uchicago, get_abstract_info_uchicago


# =============================================================================
# Scraper/Saver
# =============================================================================
def scrape_uchicago_journal(journal_name, volumes, issues):
    """
    Scrapes information from University of Chicago journal webpages and saves it in a JSON file.

    Args:
        journal_name (str): The name of the journal to scrape.
        volumes (list of int): Volumes to scrape.
        issues (list of int or None): Issues to scrape within each volume.

    Returns:
        None: Saves the scraped data as a JSON file in the DATA_PATH directory.
    """

    output_path = os.path.join(DATA_PATH, f'uchicago_{journal_name}.json')
    journal_url = 'https://www.journals.uchicago.edu/toc/{}/{{}}/{{}}'.format(journal_name)

    html_list = []
    abstract_list = []
    url = []

    # Generate URLs
    try:
        for volume in volumes:
            if issues:
                for issue in issues:
                    url.append(journal_url.format(volume, issue))
            else:
                url.append(journal_url.format(volume))
    except Exception as e:
        raise RuntimeError(f"URL generation failed: {e}")

    # Get links for each paper with progress bar
    for site in tqdm(url, desc="Getting paper links"):
        try:
            html_list = get_papers_link_uchicago(site, html_list, 5)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_uchicago(url_paper_list=html_list, paper_number=i, wait_time=15)
            if abstract:
                abstract_list.append(abstract)
        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)


# =============================================================================
# Run Multiple
# =============================================================================
def scrape_multiple_uchicago_journals(journal_list, volumes, issues):
    """
    Scrapes multiple University of Chicago journals for academic articles.

    Args:
        journal_list (list of str): List of journal names to scrape.
        volumes (list of int): Volumes to scrape in each journal.
        issues (list of int): Issues to scrape within each volume.

    Returns:
        None: Saves the scraped data as JSON files for each journal.
    """
    for journal_name in journal_list:
        print(f"Starting {journal_name}")
        scrape_uchicago_journal(journal_name, volumes, issues)


# =============================================================================
# Main
# =============================================================================
def main():
    volumes = [41]
    issues = [4]

    uchicago_journals = ['edcc', 'jole', 'jle', 'jpe', 'ntj', 'reep']

    scrape_uchicago_journal(journal_name='jole', volumes=volumes, issues=issues)
    # scrape_multiple_uchicago_journals(uchicago_journals, volumes, issues)


if __name__ == "__main__":
    main()
