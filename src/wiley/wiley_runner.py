# -*- coding: utf-8 -*-

"""
Wiley Journal Web Scraper

This module provides automated tools for scraping academic articles from Wiley journals.
It extracts details such as article titles, authors, abstracts, and issue/volume information using Python, Selenium,
and the Firefox web driver. The scraped data is saved in JSON format. The module includes functions for both
manual and automatic scraping of articles from specified journals.

Functions:
    scrape_multiple_wiley_journals(journal_list, num_prev_vols, wait_time): Scrapes multiple Wiley journals based on a provided list of journal names.
    automatic_scrape_wiley_journal(name, num_prev_vols, wait_time): Automatically scrapes articles from a specified Wiley journal.
    manual_scrape_wiley_journals(name, volumes, issues, wait_time): Manually scrapes articles from a specified Wiley journal based on provided volumes and issues.

Usage:
    To scrape multiple journals automatically:
        journal_list = ['journal1', 'journal2', ...]
        scrape_multiple_wiley_journals(journal_list, num_prev_vols, wait_time)

    To scrape a single journal:
        scrape_wiley_journal('journal-name', automatic_collection, num_prev_vols, manual_vols, manual_issues, wait_time)
"""

# =============================================================================
# Packages
# =============================================================================

# General Modules
from tqdm import tqdm
import json
import os.path
import pandas as pd

# Developed Modules
from config import USER_PATH, DATA_PATH
from src.wiley.web_scrapper_wiley import get_latest_volume_number_wiley, get_num_issues_wiley, \
    get_paper_number_from_name_wiley, get_papers_link_wiley, get_abstract_info_wiley
from src.helperFunctions.saving_to_dfs import process_file

# =============================================================================
# Scraper/Saver Functions
# =============================================================================

def automatic_scrape_wiley_journal(name, num_prev_vols, wait_time):
    """
    Automatically scrapes articles from a specified Wiley journal.

    Args:
        name (str): The name of the Wiley journal.
        num_prev_vols (int): The number of previous volumes to scrape.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        None: Saves the scraped data as a JSON file.
    """


    int_paper = get_paper_number_from_name_wiley(name)
    volume_url = f"https://onlinelibrary.wiley.com/journal/{int_paper}"
    journal_url = "https://onlinelibrary.wiley.com/toc/{}/{{}}/{{}}".format(int_paper)
    output_path = os.path.join(DATA_PATH, f'wiley_{name}.json')
    output_path_solo_df = os.path.join(DATA_PATH, f'wiley_df.csv')
    output_path_total_df = os.path.join(DATA_PATH, f'all_df.csv')

    html_list = []
    abstract_list = []
    url = []

    num_issues = get_num_issues_wiley(name)
    issues = [i for i in range(1, num_issues + 1)]
    latest_vol = get_latest_volume_number_wiley(volume_url, wait_time)
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
            html_list = get_papers_link_wiley(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_wiley(url_paper_list=html_list, paper_number=i, wait_time=wait_time)
            if abstract:
                abstract_list.append(abstract)


        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)

    #ToDo add UNIQUE KEY

    # Convert to DataFrame
    df = pd.DataFrame(abstract_list, columns=['Volume_Issue', 'Details'])
    df[['Title', 'Authors', 'Abstract']] = pd.DataFrame(df['Details'].tolist(), index=df.index)
    df.drop(columns=['Details'], inplace=True)

    df.insert(0, 'Journal_Website', 'Wiley')
    df.insert(1, 'Journal_Name', name)

    columns = ['Journal_Website', 'Journal_Name', 'Volume_Issue', 'Title', 'Authors', 'Abstract']

    process_file(output_path_solo_df, df, columns)
    process_file(output_path_total_df, df, columns)


def manual_scrape_wiley_journals(name, volumes, issues, wait_time):
    """
    Manually scrapes articles from a specified Wiley journal based on provided volumes and issues.

    Args:
        name (str): The name of the Wiley journal.
        volumes (list of int): Volumes to scrape.
        issues (list of int): Issues to scrape within each volume.
        wait_time (int): Time to wait for page rendering before scraping.

    Returns:
        None: Saves the scraped data as a JSON file.
    """

    int_paper = get_paper_number_from_name_wiley(name)
    journal_url = "https://onlinelibrary.wiley.com/toc/{}/{{}}/{{}}".format(int_paper)
    output_path = os.path.join(DATA_PATH, f'wiley_{name}.json')

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
            html_list = get_papers_link_wiley(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_wiley(url_paper_list=html_list, paper_number=i, wait_time=wait_time)
            if abstract:
                abstract_list.append(abstract)
        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)

    # #ToDo add saving in XLSX
    #
    # # Convert to DataFrame
    # df = pd.DataFrame(abstract_list, columns=['Volume_Issue', 'Details'])
    # df[['Title', 'Authors', 'Abstract']] = pd.DataFrame(df['Details'].tolist(), index=df.index)
    # df.drop(columns=['Details'], inplace=True)
    #
    #
    # df['Journal_Website'] = 'Wiley'
    # df['Journal_Name'] = name
    #
    # process_file(output_path_solo_df, df)
    # process_file(output_path_total_df, df)


# =============================================================================
# Run Multiple
# =============================================================================
def scrape_multiple_wiley_journals(journal_list, num_prev_vols, wait_time):
    for name in journal_list:
        try:
            automatic_scrape_wiley_journal(name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)

def main():
    journal_list = ['The Journal of Finance',
                    'Journal of Money, Credit and Banking',
                    'RAND Journal of Economics',
                    'Journal of Applied Econometrics',
                    'International Economic Review',
                    'Oxford Bulletin of Economics and Statistics',
                    'Journal of Economic Surveys',
                    'Journal of Accounting Research',
                    'Quantitative Economics',
                    'Journal of Industrial Economics',
                    'Scandinavian Journal of Economics',
                    'Journal of Economics & Management Strategy',
                    'Theoretical Economics',
                    'Economic Enquiry',
                    'American Journal of Agricultural Economics',
                    'Economics and Politics',
                    'Canadian Journal of Economics',
                    'Journal of Forecasting']

    scrape_multiple_wiley_journals(journal_list, 1, 15)


if __name__ == "__main__":
    main()
