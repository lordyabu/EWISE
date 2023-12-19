# -*- coding: utf-8 -*-

# =============================================================================
# Elsevier Journal Web Scraper
# =============================================================================
"""
This module provides automated tools for scraping academic articles from
Elsevier journals. It extracts details like article titles, authors, abstracts,
and issue/volume information using Selenium with GeckoDriver for web scraping.
The scraped data is saved in JSON format.

Functions:
    scrape_elsevier_journal(journal_name, volumes, issues): Main function to scrape
        articles from a specified Elsevier journal.
    scrape_multiple_elsevier_journals(journal_list, volumes, issues): Scrapes multiple
        journals based on the given list of journal names.

Usage:
    To scrape a single journal:
        scrape_elsevier_journal('journal-name', [volume_numbers], [issue_numbers])

    To scrape multiple journals:
        journal_list = ['journal1', 'journal2', ...]
        scrape_multiple_elsevier_journals(journal_list, [volume_numbers], [issue_numbers])
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
from src.elsevier.web_scrapper_elsevier import get_papers_link_elsevier, get_abstract_info_elsevier


# =============================================================================
# Scraper/Saver
# =============================================================================
def scrape_elsevier_journal(journal_name, volumes, issues):
    """
    Scrapes a specified Elsevier journal for academic articles.

    Args:
        journal_name (str): The name of the journal.
        volumes (list of int): Volumes to scrape.
        issues (list of int): Issues to scrape within each volume.

    Returns:
        None: Saves the scraped data as a JSON file.
    """

    output_path = os.path.join(DATA_PATH, f'elsevier_{journal_name}.json')
    journal_url = 'https://www.sciencedirect.com/journal/{}/vol/{{}}/suppl/C'.format(journal_name)

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
            html_list = get_papers_link_elsevier(site, html_list, 5)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_elsevier(url_paper_list=html_list, paper_number=i, wait_time=3)
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
def scrape_multiple_elsevier_journals(journal_list, volumes, issues):
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
        scrape_elsevier_journal(journal_name, volumes, issues)


# =============================================================================
# Main
# =============================================================================
def main():
    journal_list = ["journal-of-empirical-finance", 'journal-of-economic-behavior-and-organization',
                    'journal-of-economic-dynamics-and-control', 'journal-of-economic-theory',
                    'journal-of-environmental-economics-and-management', 'journal-of-health-economics',
                    'journal-of-international-economics', 'journal-of-international-money-and-finance',
                    'journal-of-mathematical-economics', 'journal-of-monetary-economics', 'journal-of-public-economics',
                    'journal-of-econometrics', 'journal-of-development-economics', 'asia-and-the-global-economy',
                    'journal-of-accounting-and-economics', 'journal-of-financial-markets', 'journal-of-macroeconomics',
                    'journal-of-economics-and-business', 'journal-of-financial-economics', 'economic-modelling']
    volumes = [70]
    issues = [0]

    scrape_multiple_elsevier_journals(journal_list=journal_list, volumes=volumes, issues=issues)


if __name__ == "__main__":
    main()
