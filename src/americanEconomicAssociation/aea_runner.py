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


def automatic_scrape_aea_journal(name, num_prev_vols, wait_time):
    journal_url = f'https://www.aeaweb.org/journals/{name}/issues'

    output_path = os.path.join(DATA_PATH, f'aea_{name}.json')

    aea_dict = get_volume_and_issue_data_aea(journal_url)

    if len(aea_dict.keys()) == 0:
        raise KeyError(f"Journal {name} does not have any data")

    html_list = []
    abstract_list = []
    url = []

    count = 0

    if len(url) == 0:
        for vol in aea_dict.keys():
            for issue_data in aea_dict[vol]:
                url.append(issue_data[1])

            count += 1
            if count == num_prev_vols:
                break

    # Get links for each paper with progress bar
    for site in tqdm(url, desc="Getting paper links"):
        try:
            html_list = get_papers_link_aea(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_aea(url_paper_list=html_list, paper_number=i, wait_time=wait_time)
            if abstract:
                abstract_list.append(abstract)
        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)


def manual_scrape_aea_journal(name, volumes, issues, wait_time):
    """
    Scrapes a specified Elsevier journal for academic articles.

    Args:
        journal_name (str): The name of the journal.
        volumes (list of int): Volumes to scrape.
        issues (list of int): Issues to scrape within each volume.

    Returns:
        None: Saves the scraped data as a JSON file.
    """

    journal_url = f'https://www.aeaweb.org/journals/{name}/issues'

    output_path = os.path.join(DATA_PATH, f'aea_{name}.json')

    aea_dict = get_volume_and_issue_data_aea(journal_url)

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

    # Get links for each paper with progress bar
    for site in tqdm(url, desc="Getting paper links"):
        try:
            html_list = get_papers_link_aea(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_aea(url_paper_list=html_list, paper_number=i, wait_time=wait_time)
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
def scrape_multiple_aea_journals(journal_list, num_prev_vols, wait_time):
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
        try:
            automatic_scrape_aea_journal(journal_name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)


# =============================================================================
# Main
# =============================================================================
def main():
    # volumes = [61]
    # issues = [4]

    aea_journals = ['jel', 'mac', 'aeri', 'pol', 'app', 'mic', 'jep', 'aer']

    # scrape_aea_journal(journal_name='jel', volumes=volumes, issues=issues, get_link_dicts=False)
    scrape_multiple_aea_journals(aea_journals, 1, 30)


if __name__ == "__main__":
    main()
