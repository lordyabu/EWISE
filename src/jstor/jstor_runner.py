# -*- coding: utf-8 -*-


# Currently not in use ///////////////////////////////////


# =============================================================================
# Jstor Journal Web Scraper
# =============================================================================
"""
This module provides a web scraping tool to extract data from academic
journals hosted on JSTOR. It uses Python with the Selenium library and
Firefox web driver to automate the process of accessing journal webpages
and collecting information such as article titles, authors, abstracts, and
issue/volume details. The data is saved in JSON format.

Functions:
    scrape_jstor_journal(journal_name, volumes, issues, get_link_dicts=True): Scrapes articles
        from a specified JSTOR journal.

Usage:
    To scrape a specific journal:
        scrape_jstor_journal('journal-name', [volume_numbers], [issue_numbers])
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
from src.helperFunctions.jsonHelpers import save_dict_as_json, load_json_as_dict
from src.jstor.web_scraper_jstor import get_papers_link_jstor, get_abstract_info_jstor, get_volume_and_issue_data_jstor, \
    get_link_from_dict_jstor


# =============================================================================
# Scraper/Saver
# =============================================================================
def scrape_jstor_journal(journal_name, volumes, issues, get_link_dicts=True):
    """
    Scrapes information from JSTOR journal webpages and saves it in a JSON file.

    Args:
        journal_name (str): End of link for specific journal.
        volumes (list of int): Volume numbers to scrape.
        issues (list of int): Issue numbers within each volume to scrape.
        get_link_dicts (bool): Whether to retrieve link dictionaries.

    Returns:
        None: Saves the scraped data to a JSON file.
    """

    journal_url = f'https://www.jstor.org/journal/{journal_name}'
    output_path = os.path.join(DATA_PATH, f'jstor_{journal_name}.json')

    # Get volumne/issue links as url pattern is unclear
    if get_link_dicts:
        url_links = get_volume_and_issue_data_jstor(journal_url)
        save_dict_as_json(url_links, f'urldict_jstor_{journal_name}.json')
    url_links_loaded = load_json_as_dict(f'urldict_jstor_{journal_name}.json')

    html_list = []
    abstract_list = []
    url = []

    # Generate URLs
    try:
        for volume in volumes:
            if issues:
                for issue in issues:
                    url.append(get_link_from_dict_jstor(url_links_loaded, volume, issue))
            else:
                pass
    except Exception as e:
        raise RuntimeError(f"URL generation failed: {e}")

    # Get links for each paper with progress bar
    for site in tqdm(url, desc="Getting paper links"):
        try:
            html_list = get_papers_link_jstor(site, html_list, 30)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_jstor(url_paper_list=html_list, paper_number=i, wait_time=30)
            if abstract:
                abstract_list.append(abstract)
        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)


# =============================================================================
# Main
# =============================================================================
def main():
    volumes = [58]
    issues = [4]

    scrape_jstor_journal(journal_name='jeconlite', volumes=volumes, issues=issues)


if __name__ == "__main__":
    main()
