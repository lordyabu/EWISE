# -*- coding: utf-8 -*-

"""
Springer Journal Web Scraper

This module provides automated tools for scraping academic articles from Springer journals. It extracts details such as article titles,
authors, abstracts, and issue/volume information using Selenium with GeckoDriver for web scraping. The scraped data is saved in JSON format.
The module includes functions for both manual and automatic scraping of articles from specified journals.

Functions:
    automatic_scrape_springer_journal(name, num_prev_vols, wait_time): Automatically scrapes articles from a specified Springer journal.
    manual_scrape_springer_journals(name, volumes, issues, wait_time): Manually scrapes articles from a specified Springer journal based on provided volumes and issues.
    scrape_multiple_springer_journals(journal_list, num_prev_vols, wait_time): Scrapes multiple Springer journals based on a provided list of journal names.

Usage:
    To scrape a single journal automatically:
        automatic_scrape_springer_journal('journal-name', num_prev_vols, wait_time)

    To scrape a single journal manually:
        manual_scrape_springer_journals('journal-name', [volume_numbers], [issue_numbers], wait_time)

    To scrape multiple journals automatically:
        journal_list = ['journal1', 'journal2', ...]
        scrape_multiple_springer_journals(journal_list, num_prev_vols, wait_time)
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
from src.springer.web_scraper_springer import get_latest_volume_number_springer, get_num_issues_springer, \
    get_paper_number_from_name_springer, get_papers_link_springer, get_abstract_info_springer
from src.helperFunctions.saving_to_dfs import process_file

# =============================================================================
# Scraper/Savers
# =============================================================================

def automatic_scrape_springer_journal(name, num_prev_vols, wait_time):
    int_paper = get_paper_number_from_name_springer(name)
    volume_url = f"https://link.springer.com/journal/{int_paper}/volumes-and-issues"
    journal_url = "https://link.springer.com/journal/{}/volumes-and-issues/{{}}-{{}}".format(int_paper)
    output_path = os.path.join(DATA_PATH, f'springer_{name}.json')
    output_path_solo_df = os.path.join(DATA_PATH, f'springer_df.csv')
    output_path_total_df = os.path.join(DATA_PATH, f'all_df.csv')

    html_list = []
    abstract_list = []
    url = []

    num_issues = get_num_issues_springer(name)
    issues = [i for i in range(1, num_issues + 1)]
    latest_vol = get_latest_volume_number_springer(volume_url, wait_time)
    starting_vol = max(1, latest_vol - num_prev_vols + 1)
    volumes = [vol for vol in range(starting_vol, latest_vol + 1)]

    print(latest_vol)

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
            html_list = get_papers_link_springer(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_springer(url_paper_list=html_list, paper_number=i, wait_time=wait_time, journal_name=name)
            if abstract:
                abstract_list.append(abstract)
                #ToDo remove
                break
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

    df.insert(0, 'Journal_Website', 'Springer')
    df.insert(1, 'Journal_Name', name)

    # columns = ['Journal_Website', 'Journal_Name', 'Key', 'Volume_Issue', 'Title', 'Authors', 'Abstract']
    columns = ['Journal_Website', 'Journal_Name', 'Volume_Issue', 'Title', 'Authors', 'Abstract']


    process_file(output_path_solo_df, df, columns)
    process_file(output_path_total_df, df, columns)


def manual_scrape_springer_journals(name, volumes, issues, wait_time):
    int_paper = get_paper_number_from_name_springer(name)
    journal_url = "https://link.springer.com/journal/{}/volumes-and-issues/{{}}-{{}}".format(int_paper)
    output_path = os.path.join(DATA_PATH, f'springer_{name}.json')

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
            html_list = get_papers_link_springer(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_springer(url_paper_list=html_list, paper_number=i, wait_time=wait_time)
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
def scrape_multiple_springer_journals(journal_list, num_prev_vols, wait_time):
    for name in journal_list:
        try:
            automatic_scrape_springer_journal(name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)


# =============================================================================
# Main
# =============================================================================
def main():
    journal_list = ['IMF Economic Review', 'Journal of Economic Growth', 'Journal of Risk and Uncertainty',
                    'Journal of Population Economics', 'Economic Theory', 'Public Choice', 'Empirical Economics']
    scrape_multiple_springer_journals(journal_list, 1, 15)


if __name__ == "__main__":
    main()
