# -*- coding: utf-8 -*-

"""
American Economic Association (AEA) Journal Web Scraper

This module provides automated tools for scraping academic articles from AEA journals. It extracts article titles, authors, abstracts,
and issue/volume information using Selenium with GeckoDriver for web scraping. The scraped data is saved in JSON format. The module
includes functions for both manual and automatic scraping of articles from specified journals.

Functions:
    automatic_scrape_aea_journal(name, num_prev_vols, wait_time): Automatically scrapes articles from a specified AEA journal.
    manual_scrape_aea_journal(name, volumes, issues, wait_time): Manually scrapes articles from a specified AEA journal based on provided volumes and issues.
    scrape_multiple_aea_journals(journal_list, num_prev_vols, wait_time): Scrapes multiple journals based on a provided list of journal names.

Usage:
    To scrape a single journal automatically:
        automatic_scrape_aea_journal('journal-name', num_prev_vols, wait_time)

    To scrape a single journal manually:
        manual_scrape_aea_journal('journal-name', [volume_numbers], [issue_numbers], wait_time)

    To scrape multiple journals automatically:
        journal_list = ['journal1', 'journal2', ...]
        scrape_multiple_aea_journals(journal_list, num_prev_vols, wait_time)
"""

# =============================================================================
# Packages
# =============================================================================

# General Modules
import os.path
import sys
import json
from tqdm import tqdm
import pandas as pd

# Developed Modules
from config import USER_PATH, DATA_PATH
sys.path.append(os.path.join(USER_PATH, 'src'))
from src.americanEconomicAssociation.web_scraper_aea import get_papers_link_aea, get_abstract_info_aea, \
    get_volume_and_issue_data_aea
from src.helperFunctions.saving_to_dfs import process_file
from src.helperFunctions.generateKey import generate_key


# =============================================================================
# Scraper/Savers
# =============================================================================


def automatic_scrape_aea_journal(name, num_prev_vols, wait_time):
    """
    Automatically scrapes articles from a specified AEA journal.

    Args:
        name (str): The name of the AEA journal.
        num_prev_vols (int): The number of previous volumes to scrape.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        None: Saves the scraped data as a JSON file.
    """

    journal_url = f'https://www.aeaweb.org/journals/{name}/issues'

    output_path = os.path.join(DATA_PATH, f'aea_{name}.json')
    output_path_solo_df = os.path.join(DATA_PATH, f'aea_df.csv')
    output_path_total_df = os.path.join(DATA_PATH, f'all_df.csv')

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
            abstract = get_abstract_info_aea(url_paper_list=html_list, paper_number=i, wait_time=wait_time, journal_name=name)
            if abstract:
                abstract_list.append(abstract)
        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)



    # Convert to DataFrame
    df = pd.DataFrame(abstract_list, columns=['Volume_Issue', 'Details'])
    # df = pd.DataFrame(abstract_list, columns=['Key', 'Volume_Issue', 'Details'])
    df[['Title', 'Authors', 'Abstract']] = pd.DataFrame(df['Details'].tolist(), index=df.index)
    df.drop(columns=['Details'], inplace=True)

    df.insert(0, 'Journal_Website', 'American Economic Association')

    #ToDo reformat name
    
    df.insert(1, 'Journal_Name', name)

    # columns = ['Journal_Website', 'Journal_Name', 'Key', 'Volume_Issue', 'Title', 'Authors', 'Abstract']
    columns = ['Journal_Website', 'Journal_Name', 'Volume_Issue', 'Title', 'Authors', 'Abstract']

    process_file(output_path_solo_df, df, columns)
    process_file(output_path_total_df, df, columns)


def manual_scrape_aea_journal(name, volumes, issues, wait_time):
    """
    Manually scrapes articles from a specified AEA journal based on provided volumes and issues.

    Args:
        name (str): The name of the AEA journal.
        volumes (list of int): Volumes to scrape.
        issues (list of int): Issues to scrape within each volume.
        wait_time (int): Time to wait for page rendering before scraping.

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

    #ToDo add saving in XLSX

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
