# -*- coding: utf-8 -*-

# =============================================================================
# American Economic Association (AEA) Journal Web Scraper
# =============================================================================
"""
This module provides automated tools for scraping academic articles from AEA journals.
It extracts article titles, authors, abstracts, and issue/volume information using Selenium
with GeckoDriver. The scraped data is saved in JSON format.

Functions:
    scrape_aea_journal(journal_name, volumes, issues, get_link_dicts=True): Main function
        to scrape articles from a specified AEA journal.
    scrape_multiple_aea_journals(journal_list, volumes, issues): Scrapes multiple journals
        based on the given list of journal names.

Usage:
    To scrape a single journal:
        scrape_aea_journal('journal-name', [volume_numbers], [issue_numbers])

    To scrape multiple journals:
        journal_list = ['journal1', 'journal2', ...]
        scrape_multiple_aea_journals(journal_list, [volume_numbers], [issue_numbers])
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
from src.helperFunctions.jsonHelpers import load_json_as_dict, save_dict_as_json

# Developed Modules
sys.path.append(os.path.join(USER_PATH, 'src'))
from src.americanEconomicAssociation.web_scraper_aea import get_papers_link_aea, get_abstract_info_aea, \
    get_volume_and_issue_data_aea


# =============================================================================
# Scraper/Saver
# =============================================================================
def scrape_aea_journal(journal_name, volumes, issues, get_link_dicts=True):
    """
    Scrapes a specified Elsevier journal for academic articles.

    Args:
        journal_name (str): The name of the journal.
        volumes (list of int): Volumes to scrape.
        issues (list of int): Issues to scrape within each volume.

    Returns:
        None: Saves the scraped data as a JSON file.
    """

    journal_url = f'https://www.aeaweb.org/journals/{journal_name}/issues'

    output_path = os.path.join(DATA_PATH, f'aea_{journal_name}.json')

    if get_link_dicts:
        url_links = get_volume_and_issue_data_aea(journal_url)

        save_dict_as_json(url_links, f'urldict_aea_{journal_name}.json')

    aea_dict = load_json_as_dict(f'urldict_aea_{journal_name}.json')

    html_list = []
    abstract_list = []
    url = []

    for volume in volumes:
        volume_key = f"Volume {volume}"
        if volume_key in aea_dict:
            for issue in issues:
                for issue_data in aea_dict[volume_key]:
                    if issue_data[0] == str(issue):
                        url.append(issue_data[1])

    # ToDo: Modify this to take last X volumes.
    # If no urls found, get from the latest volume
    if len(url) == 0:
        for vol in aea_dict.keys():
            for issue in issues:
                for issue_data in aea_dict[vol]:
                    if issue_data[0] == str(issue):
                        url.append(issue_data[1])
                        break
                break
            break


    # Get links for each paper with progress bar
    for site in tqdm(url, desc="Getting paper links"):
        try:
            html_list = get_papers_link_aea(site, html_list, 30)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")


    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_aea(url_paper_list=html_list, paper_number=i, wait_time=30)
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
def scrape_multiple_aea_journals(journal_list, volumes, issues):
    """
    Scrapes multiple AEA journals for academic articles.

    Args:
        journal_list (list of str): List of journal names to scrape.
        volumes (list of int): Volumes to scrape in each journal.
        issues (list of int): Issues to scrape within each volume.

    Returns:
        None: Saves the scraped data as JSON files for each journal.
    """
    for journal_name in journal_list:
        print(f"Starting {journal_name}")
        scrape_aea_journal(journal_name, volumes, issues)


# =============================================================================
# Main
# =============================================================================
def main():
    volumes = [61]
    issues = [4]

    aea_journals = ['mac', 'aeri', 'pol', 'app', 'mic', 'jep']

    scrape_aea_journal(journal_name='jel', volumes=volumes, issues=issues, get_link_dicts=False)
    # scrape_multiple_aea_journals(aea_journals, volumes, issues)


if __name__ == "__main__":
    main()
