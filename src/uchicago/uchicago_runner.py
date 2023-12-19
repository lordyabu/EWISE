# -*- coding: utf-8 -*-
"""
Web Scapper for Academic Journals

This project provides a web scraping tool to extract data from academic
journals, including article titles, authors, abstracts, and other details.
It uses the Python programming language and the Selenium library,
along with the Firefox web driver, to automate the process of accessing
academic journal webpages and collecting relevant information.

"""
import os.path
# =============================================================================
# Packages
# =============================================================================

# General Modules
import sys
import json
from tqdm import tqdm
from config import USER_PATH, DATA_PATH
from src.helperFunctions.jsonHelpers import load_json_as_dict, save_dict_as_json
# Developed Modules

sys.path.append(os.path.join(USER_PATH, 'src'))
from src.uchicago.web_scrapper_uchicago import get_papers_link_uchicago, get_abstract_info_uchicago

# =============================================================================
# Parameters
# =============================================================================
#
# 1 - URL with the journal issue and volume as paramter
# need_to_get_volume_links = True
# journal_url = 'https://www.journals.uchicago.edu/toc/jole/{}/{}'
# #
# # if need_to_get_volume_links:
# #     vol_link_dict = get_volume_and_issue_data_aea(journal_url)
# #     save_dict_as_json(vol_link_dict, 'urldict_aea_jel.json')
# #
# # # 2 - Start empty list with link for each paper
# html_list = []
# abstract_list = []
# #
# # # 3 - Issues and Volumes availables
# volumes = [39]
# # # issues = [1,2,3,4]
# issues = [4]
# #
# # # 4 - HTML Div IDs
# # #
# # # # =============================================================================
# # # # Application
# # # # =============================================================================
# # #
# #
# # jel_dict = load_json_as_dict('urldict_aea_jel.json')
# #
# url = []
# #
# # # # 1 - Generate strings for each volume and issue (choose either 1.1 or 1.2)
# # #
# # # ## 1.1 - With volume and issues
# try:
#     for volume in volumes:
#         for issue in issues:
#             url.append(journal_url.format(volume, issue))
# except:
#     pass
#
# # #
# # # ## 1.2 - With only volumes
# # # # try:
# # # #     for volume in volumes:
# # # #         url.append(journal_url.format(volume))
# # # # except:
# # # #     pass
# # #
# # # ## 2 - Get links for each paper
# try:
#     for site in url:
#         print(site)
#         html_list = get_papers_link_uchicago(site, html_list, 1)
# except:
#     pass
# #
#
# print("html list done", html_list)
# #
# #
# # 3 - Get Abstracts from step 2
# try:
#     for i in range(1, len(html_list)):
#         print("attempting")
#         abstract = get_abstract_info_uchicago(url_paper_list=html_list, paper_number=i, wait_time=10)
#         print(abstract, 'abstract got')
#         if abstract:
#             break
#         abstract_list.append(abstract)
# except:
#     pass

# =============================================================================
# =============================================================================

def scrape_uchicago_journal(journal_name, volumes, issues):
    """
    Scrapes information from Elsevier journal webpages and saves it in a JSON file.

    This function automates the process of accessing Elsevier journal webpages to collect
    detailed information about academic articles. It uses Selenium with GeckoDriver for
    web scraping. The information collected includes article titles, authors, abstracts,
    and issue/volume details. The progress of scraping is displayed using a progress bar.

    Args:
        journal_name (str): The name of the journal to scrape. This name is used in the
                            URL to access specific journal pages.
        volumes (list of int): A list of volume numbers to scrape. Each volume number
                               corresponds to a volume of the journal.
        issues (list of int or None): A list of issue numbers to scrape within each volume.
                                      If None or empty, all issues in the specified volumes
                                      will be scraped.
        title_id (str): The HTML element ID for locating the title of an article on the webpage.
        author_id (str): The HTML element ID for locating the authors of an article.
        abstract_id (str): The HTML element ID for locating the abstract of an article.
        issue_vol_id (str): The HTML element ID for locating the issue and volume information
                            of an article.

    Returns:
        None: The function does not return any value. Instead, it writes the scraped data to
              a JSON file named 'elsevier_{journal_name}.json' in the directory specified by the global
              variable DATA_PATH.
    """

    output_path = os.path.join(DATA_PATH, f'uchicago_{journal_name}.json')
    journal_url = 'https://www.journals.uchicago.edu/toc/{}/{{}}/{{}}'.format(journal_name)

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
            html_list = get_papers_link_uchicago(site, html_list, 5)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_uchicago(url_paper_list=html_list, paper_number=i, wait_time=15)
            if abstract:
                abstract_list.append(abstract)
                break
        except Exception as e:
            pass
    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)

def scrape_multiple_uchicago_journals(journal_list, volumes, issues):
    for journal_name in journal_list:
        print(f"Starting {journal_name}")
        scrape_uchicago_journal(journal_name, volumes, issues)

def main():
    volumes = [41]
    issues = [4]

    uchicago_journals = ['edcc', 'jole', 'jle', 'jpe', 'ntj', 'reep']

    # scrape_uchicago_journal(journal_name='jole', volumes=volumes, issues=issues)
    scrape_multiple_uchicago_journals(uchicago_journals, volumes, issues)


if __name__ == "__main__":
    main()