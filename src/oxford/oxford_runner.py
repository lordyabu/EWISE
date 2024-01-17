# -*- coding: utf-8 -*-

"""
Oxford Journal Web Scraper

This module provides automated tools for scraping academic articles from Oxford journals. It extracts details such as article titles,
authors, abstracts, and issue/volume information using Selenium with GeckoDriver for web scraping. The scraped data is saved in JSON format.
The module includes functions for both manual and automatic scraping of articles from specified journals.

Functions:
    automatic_scrape_oxford_journal(name, num_prev_vols, wait_time): Automatically scrapes articles from a specified Oxford journal.
    manual_scrape_oxford_journals(name, volumes, issues, wait_time): Manually scrapes articles from a specified Oxford journal based on provided volumes and issues.
    scrape_multiple_oxford_journals(journal_list, num_prev_vols, wait_time): Scrapes multiple Oxford journals based on a provided list of journal names.

Usage:
    To scrape a single journal automatically:
        automatic_scrape_oxford_journal('journal-name', num_prev_vols, wait_time)

    To scrape a single journal manually:
        manual_scrape_oxford_journals('journal-name', [volume_numbers], [issue_numbers], wait_time)

    To scrape multiple journals automatically:
        journal_list = ['journal1', 'journal2', ...]
        scrape_multiple_oxford_journals(journal_list, num_prev_vols, wait_time)
"""

# =============================================================================
# Packages
# =============================================================================

# General Modules
import os.path
import sys
import json
from tqdm import tqdm

# Developed Modules
from config import USER_PATH, DATA_PATH
sys.path.append(os.path.join(USER_PATH, 'src'))
from src.oxford.web_scraper_oxford import get_papers_link_oxford, get_abstract_info_oxford, \
    get_latest_volume_number_oxford, \
    get_num_issues_oxford


# =============================================================================
# Scraper/Savers
# =============================================================================
def automatic_scrape_oxford_journal(name, num_prev_vols, wait_time):
    """
    Automatically scrapes articles from a specified Oxford journal.

    Args:
        name (str): The name of the Oxford journal.
        num_prev_vols (int): The number of previous volumes to scrape.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        None: Saves the scraped data as a JSON file.
    """

    base_url = f"https://academic.oup.com/{name}"
    output_path = os.path.join(DATA_PATH, f'oxford_{name}.json')
    journal_url = "{}/issue/{{}}/{{}}".format(base_url)

    html_list = []
    abstract_list = []
    url = []

    num_issues = get_num_issues_oxford(name)

    # The Economic Journal does not reset issue # every volume
    if num_issues == "NY":
        raise ValueError("The Economic Journal is not supported yet")
        # issues = ['']
    else:
        issues = [i for i in range(1, num_issues + 1)]

    latest_vol = get_latest_volume_number_oxford(base_url, wait_time)
    starting_vol = max(1, latest_vol - num_prev_vols + 1)
    volumes = [vol for vol in range(starting_vol, latest_vol + 1)]

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

    # Get links for each paper
    for site in tqdm(url, desc="Getting paper links"):
        try:
            html_list = get_papers_link_oxford(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_oxford(url_paper_list=html_list, paper_number=i, wait_time=wait_time)
            if abstract:
                abstract_list.append(abstract)
        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)

    #ToDo add saving in XLSX

def manual_scrape_oxford_journals(name, volumes, issues, wait_time):
    """
    Manually scrapes articles from a specified Oxford journal based on provided volumes and issues.

    Args:
        name (str): The name of the Oxford journal.
        volumes (list of int): Volumes to scrape.
        issues (list of int): Issues to scrape within each volume.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        None: Saves the scraped data as a JSON file.
    """

    if name == "ej":
        raise ValueError("The Economic Journal is not supported yet")

    base_url = f"https://academic.oup.com/{name}"
    output_path = os.path.join(DATA_PATH, f'oxford_{name}.json')
    journal_url = "{}/issue/{{}}/{{}}".format(base_url)

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

    # Get links for each paper
    for site in tqdm(url, desc="Getting paper links"):
        try:
            html_list = get_papers_link_oxford(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_oxford(url_paper_list=html_list, paper_number=i, wait_time=wait_time)
            if abstract:
                abstract_list.append(abstract)
        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)

    #ToDo add saving in XLSX


# =============================================================================
# Run Multiple
# =============================================================================
def scrape_multiple_oxford_journals(journal_list, num_prev_vols, wait_time):
    """
    Scrapes multiple Oxford journals for academic articles.

    Args:
        journal_list (list of str): List of Oxford journal names to scrape.
        num_prev_vols (int): Number of previous volumes to scrape for each journal.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        None: Saves the scraped data as JSON files for each journal.
    """

    for name in journal_list:
        try:
            automatic_scrape_oxford_journal(name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)


# =============================================================================
# Main
# =============================================================================
def main():
    journal_list = ["restud", "rfs", "jeea", "wber", "jleo", "rof", "jcr", "ectj", "joeg", "rcfs", "oep", "jfec",
                    "raps"]

    scrape_multiple_oxford_journals(journal_list, 1, 15)


if __name__ == "__main__":
    main()
