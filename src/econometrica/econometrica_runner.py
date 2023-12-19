# -*- coding: utf-8 -*-
"""
Web Scapper for Academic Journals (Econometrica)

This project provides a web scraping tool to extract data from academic
journals, including article titles, authors, abstracts, and other details.
It uses the Python programming language and the Selenium library,
along with the Firefox web driver, to automate the process of accessing
academic journal webpages and collecting relevant information.

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
from src.econometrica.web_scraper_econometrica import get_papers_link_econometrica, get_abstract_info_econometrica


# =============================================================================
# Scraper/Saver
# =============================================================================
def scrape_econometrica_journal(volumes, issues):
    """
    Scrapes information from Elsevier journal webpages and saves it in a JSON file.

    This function automates the process of accessing Elsevier journal webpages to collect
    detailed information about academic articles. It uses Selenium with GeckoDriver for
    web scraping. The information collected includes article titles, authors, abstracts,
    and issue/volume details. The progress of scraping is displayed using a progress bar.

    Args:
        volumes (list of int): A list of volume numbers to scrape. Each volume number
                               corresponds to a volume of the journal.
        issues (list of int or None): A list of issue numbers to scrape within each volume.
                                      If None or empty, all issues in the specified volumes
                                      will be scraped.

    Returns:
        None: The function does not return any value. Instead, it writes the scraped data to
              a JSON file named 'econometrica.json' in the directory specified by the global
              variable DATA_PATH.
    """

    output_path = os.path.join(DATA_PATH, f'econometrica.json')
    journal_url = 'https://onlinelibrary.wiley.com/toc/14680262/2023/{}/{}'

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

    print(url)

    # Get links for each paper with progress bar
    for site in tqdm(url, desc="Getting paper links"):
        try:
            html_list = get_papers_link_econometrica(site, html_list, 5)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_econometrica(url_paper_list=html_list, paper_number=i, wait_time=3)
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
    volumes = [91]
    issues = [6]

    scrape_econometrica_journal(volumes=volumes, issues=issues)


if __name__ == "__main__":
    main()
