# -*- coding: utf-8 -*-

# =============================================================================
# Econometrica Journal Web Scraper
# =============================================================================
"""
This module provides a web scraping tool to extract data from Econometrica, an academic journal.
It automates the process of accessing webpages and collecting information like article titles,
authors, abstracts, and issue/volume details. The tool uses Python with the Selenium library
and Firefox web driver for scraping. The extracted data is saved in JSON format.

Functions:
    scrape_econometrica_journal(volumes, issues): Scrapes articles from specified volumes
        and issues of Econometrica.

Usage:
    To scrape specific volumes and issues of Econometrica:
        scrape_econometrica_journal([volume_numbers], [issue_numbers])
"""

# =============================================================================
# Packages
# =============================================================================

# General Modules
import os.path
import sys
from tqdm import tqdm
from config import USER_PATH, DATA_PATH

# Developed Modules
sys.path.append(os.path.join(USER_PATH, 'src'))
from src.original.alex_old.econometrica.web_scraper_econometrica import get_papers_link_econometrica, get_abstract_info_econometrica


# =============================================================================
# Scraper/Saver
# =============================================================================
def scrape_econometrica_journal(volumes, issues):
    """
    Scrapes information from Econometrica journal webpages and saves it in a JSON file.

    Args:
        volumes (list of int): Volumes to scrape.
        issues (list of int or None): Issues to scrape within each volume.

    Returns:
        None: Saves the scraped data as a JSON file in the DATA_PATH directory.
    """
    output_path = os.path.join(DATA_PATH, f'econometrica.json')
    journal_url = 'https://onlinelibrary.wiley.com/toc/14680262/2023/{}/{}'

    html_list = []
    corresponding_vol_iss_list = []

    abstract_list = []
    url_vol_iss = []

    # Generate URLs
    try:
        for volume in volumes:
            if issues:
                for issue in issues:
                    url_vol_iss.append((journal_url.format(volume, issue), f'Volume {volume} | Issue {issue}'))
            else:
                url_vol_iss.append(journal_url.format(volume), f'Volume {volume}')
    except Exception as e:
        raise RuntimeError(f"URL generation failed: {e}")

    # Get links for each paper with progress bar
    for site in tqdm(url_vol_iss, desc="Getting paper links"):
        try:
            html_list, vol_iss_to_add = get_papers_link_econometrica(site[0], html_list, 5)

            # Volume/Issue not scrappable so doing a manual trick.
            corresponding_vol_iss_list.extend([site[1] for _ in range(vol_iss_to_add)])
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_econometrica(url_paper_list=html_list, paper_number=i, wait_time=3,
                                                      vol_issue=corresponding_vol_iss_list)
            if abstract:
                abstract_list.append(abstract)

                #ToDo remove
                print(abstract)
                return None

        except Exception as e:
            pass

    # Write data to JSON file
    # ToDo uncomment
    # with open(output_path, 'w') as json_file:
    #     json.dump(abstract_list, json_file)


# =============================================================================
# Main
# =============================================================================
def main():
    volumes = [91]
    issues = [5]

    scrape_econometrica_journal(volumes=volumes, issues=issues)


if __name__ == "__main__":
    main()
