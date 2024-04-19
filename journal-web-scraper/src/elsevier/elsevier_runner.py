# -*- coding: utf-8 -*-

"""
Elsevier Journal Web Scraper

This module provides automated tools for scraping academic articles from Elsevier journals. It extracts article details such as titles,
authors, abstracts, and issue/volume information using Python, Selenium, and the GeckoDriver for web scraping. The scraped data is saved
in JSON format. Two main functions allow for either manual or automatic scraping of journal articles.

Functions:
    automatic_scrape_elsevier_journal(name, num_prev_vols, wait_time): Automatically scrapes articles from a specified Elsevier journal.
    manual_scrape_elsevier_journal(name, volumes, issues, wait_time): Manually scrapes articles from a specified Elsevier journal based on provided volumes and issues.
    scrape_multiple_elsevier_journals(journal_list, num_prev_vols, wait_time): Scrapes multiple journals based on a provided list of journal names.

Usage:
    To scrape a single journal automatically:
        automatic_scrape_elsevier_journal('journal-name', num_prev_vols, wait_time)

    To scrape a single journal manually:
        manual_scrape_elsevier_journal('journal-name', [volume_numbers], [issue_numbers], wait_time)

    To scrape multiple journals automatically:
        journal_list = ['journal1', 'journal2', ...]
        scrape_multiple_elsevier_journals(journal_list, num_prev_vols, wait_time)
"""

# =============================================================================
# Packages
# =============================================================================

# General Modules
import os.path
import sys
import pandas as pd
import json
from tqdm import tqdm

# Developed Modules
from config import USER_PATH, DATA_PATH
sys.path.append(os.path.join(USER_PATH, 'src'))
from src.elsevier.web_scrapper_elsevier import get_papers_link_elsevier, get_abstract_info_elsevier, \
    get_num_issues_elsevier, get_latest_volume_elsevier, convert_elsevier_name
from src.helperFunctions.saving_to_dfs import process_file

# =============================================================================
# Scraper/Savers
# =============================================================================

def automatic_scrape_elsevier_journal(name, num_prev_vols, wait_time):
    """
    Automatically scrapes articles from a specified Elsevier journal.

    Args:
        name (str): The name of the Elsevier journal.
        num_prev_vols (int): The number of previous volumes to scrape.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        None: Saves the scraped data as a JSON file.
    """

    output_path = os.path.join(DATA_PATH, f'elsevier_{name}.csv')
    output_path_solo_df = os.path.join(DATA_PATH, f'elsevier_df.csv')
    output_path_total_df = os.path.join(DATA_PATH, f'all_df.csv')

    journal_url = 'https://www.sciencedirect.com/journal/{}/vol/{{}}/suppl/C'.format(name)
    journal_multiple_issue_url = 'https://www.sciencedirect.com/journal/{}/vol/{{}}/issue/{{}}'.format(name)

    html_list = []
    abstract_list = []
    url = []

    latest_vol = int(get_latest_volume_elsevier(name))
    starting_vol = max(1, latest_vol - num_prev_vols + 1)
    volumes = [vol for vol in range(starting_vol, latest_vol + 1)]

    if get_num_issues_elsevier(name) != "No Issues":
        num_issues = get_num_issues_elsevier(name)
        issues = [i for i in range(1, num_issues + 1)]
    else:
        issues = None

    # Generate URLs
    try:
        for volume in volumes:
            if issues:
                for issue in issues:
                    url.append(journal_multiple_issue_url.format(volume, issue))
            else:
                url.append(journal_url.format(volume))
    except Exception as e:
        raise RuntimeError(f"URL generation failed: {e}")

    # Get links for each paper with progress bar
    for site in tqdm(url, desc="Getting paper links"):
        try:
            html_list = get_papers_link_elsevier(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")
    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_elsevier(url_paper_list=html_list, paper_number=i, wait_time=wait_time, journal_name=name)
            if abstract:
                abstract_list.append(abstract)

        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)

    #ToDo add UNIQUE KEY

    # Convert to DataFrame
    # df = pd.DataFrame(abstract_list, columns=['Key', 'Volume_Issue', 'Details'])
    df = pd.DataFrame(abstract_list, columns=['Volume_Issue', 'Details'])
    df[['Title', 'Authors', 'Abstract']] = pd.DataFrame(df['Details'].tolist(), index=df.index)
    df.drop(columns=['Details'], inplace=True)

    df.insert(0, 'Journal_Website', 'Elsevier')

    #ToDo reformat name

    df.insert(1, 'Journal_Name', convert_elsevier_name(name))

    # columns = ['Journal_Website', 'Journal_Name', 'Key', 'Volume_Issue', 'Title', 'Authors', 'Abstract']
    columns = ['Journal_Website', 'Journal_Name', 'Volume_Issue', 'Title', 'Authors', 'Abstract']

    process_file(output_path_solo_df, df, columns)
    process_file(output_path_total_df, df, columns)


def manual_scrape_elsevier_journal(name, volumes, issues, wait_time):
    """
    Manually scrapes articles from a specified Elsevier journal based on provided volumes and issues.

    Args:
        name (str): The name of the Elsevier journal.
        volumes (list of int): Volumes to scrape.
        issues (list of int): Issues to scrape within each volume.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        None: Saves the scraped data as a JSON file.
    """

    output_path = os.path.join(DATA_PATH, f'elsevier_{name}.json')
    journal_url = 'https://www.sciencedirect.com/journal/{}/vol/{{}}/suppl/C'.format(name)

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
            html_list = get_papers_link_elsevier(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_elsevier(url_paper_list=html_list, paper_number=i, wait_time=wait_time)
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
def scrape_multiple_elsevier_journals(journal_list, num_prev_vols, wait_time):
    """
    Scrapes multiple Elsevier journals for academic articles.

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
            automatic_scrape_elsevier_journal(journal_name, num_prev_vols, wait_time)
        except Exception as e:
            print(f"Journal {journal_name} error")
            print(e)


# =============================================================================
# Main
# =============================================================================
def main():
    journal_list = ['journal-of-empirical-finance', 'journal-of-economic-behavior-and-organization',
                    'journal-of-economic-dynamics-and-control', 'journal-of-economic-theory',
                    'journal-of-environmental-economics-and-management', 'journal-of-health-economics',
                    'journal-of-international-economics', 'journal-of-international-money-and-finance',
                    'journal-of-mathematical-economics', 'journal-of-monetary-economics',
                    'journal-of-public-economics',
                    'journal-of-econometrics', 'journal-of-development-economics', 'asia-and-the-global-economy',
                    'journal-of-accounting-and-economics', 'journal-of-financial-markets',
                    'journal-of-macroeconomics',
                    'journal-of-economics-and-business', 'journal-of-financial-economics', 'economic-modelling',
                    'economia', 'energy-policy', 'journal-of-financial-intermediation', 'european-economic-review',
                    'review-of-economic-dynamics', 'journal-of-banking-and-finance', 'energy-economics',
                    'journal-of-urban-economics', 'games-and-economic-behavior', 'world-development',
                    'economics-letters', 'labour-economics', 'journal-of-corporate-finance', 'ecological-economics',
                    'european-journal-of-political-economy', 'international-economics', 'economics-of-education-review',
                    'international-journal-of-forecasting']
    # volumes = [70]
    # issues = [0]

    # scrape_elsevier_journal('journal-of-empirical-finance', volumes, issues)
    scrape_multiple_elsevier_journals(journal_list=journal_list, num_prev_vols=1, wait_time=15)


if __name__ == "__main__":
    main()
