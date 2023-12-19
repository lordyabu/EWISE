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
from src.americanEconomicAssociation.web_scraper_aea import get_papers_link_aea, get_abstract_info_aea, get_volume_and_issue_data_aea

# =============================================================================
# Parameters
# =============================================================================
#
# 1 - URL with the journal issue and volume as paramter
# need_to_get_volume_links = True
# journal_url = 'https://www.aeaweb.org/journals/jel/issues'
#
# if need_to_get_volume_links:
#     vol_link_dict = get_volume_and_issue_data_aea(journal_url)
#     save_dict_as_json(vol_link_dict, 'urldict_aea_jel.json')
#
# # 2 - Start empty list with link for each paper
# html_list = []
# abstract_list = []
#
# # 3 - Issues and Volumes availables
# volumes = [58]
# # issues = [1,2,3,4]
# issues = [4]
#
# # 4 - HTML Div IDs
# #
# # # =============================================================================
# # # Application
# # # =============================================================================
# #
#
# jel_dict = load_json_as_dict('urldict_aea_jel.json')
#
# url = []
#
# # Iterate through the volumes and issues to get the links
# for volume in volumes:
#     volume_key = f"Volume {volume}"
#     if volume_key in jel_dict:
#         for issue in issues:
#             for issue_data in jel_dict[volume_key]:
#                 if issue_data[0] == str(issue):
#                     url.append(issue_data[1])
#
# # Print or return the results
# print(url)
#
# # # 1 - Generate strings for each volume and issue (choose either 1.1 or 1.2)
# #
# # ## 1.1 - With volume and issues
# # try:
# #     for volume in volumes:
# #         for issue in issues:
# #             url.append(journal_url.format(volume, issue))
# # except:
# #     pass
# #
# # ## 1.2 - With only volumes
# # # try:
# # #     for volume in volumes:
# # #         url.append(journal_url.format(volume))
# # # except:
# # #     pass
# #
# # ## 2 - Get links for each paper
# try:
#     for site in url:
#         html_list = get_papers_link_aea(site, html_list, 30)
# except:
#     pass
#
# print("html list done", html_list)
# #
# # print(html_list)
# #
# # 3 - Get Abstracts from step 2
# try:
#     for i in range(1, len(html_list)):
#         print("attempting")
#         abstract = get_abstract_info_aea(url_paper_list=html_list, paper_number=i, wait_time=30)
#         print(abstract, 'abstract got')
#         break
#         abstract_list.append(abstract)
# except:
#     pass

# =============================================================================
# =============================================================================

def scrape_aea_journal(journal_name, volumes, issues, get_link_dicts=True):
    """
    Scrapes information from Aea journal webpages and saves it in a JSON file.

    This function automates the process of accessing Aea journal webpages to collect
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
              a JSON file named 'aea_{journal_name}.json' in the directory specified by the global
              variable DATA_PATH.
    """

    journal_url = f'https://www.aeaweb.org/journals/{journal_name}/issues'

    output_path = os.path.join(DATA_PATH, f'aea_{journal_name}.json')

    if get_link_dicts:
        url_links = get_volume_and_issue_data_aea(journal_url)

        save_dict_as_json(url_links, f'urldict_aea_{journal_name}.json')

    aea_dict = load_json_as_dict(f'urldict_aea_{journal_name}.json')

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

    if len(url) == 0:
        for vol in aea_dict.keys():
            for issue in issues:
                for issue_data in aea_dict[vol]:
                    if issue_data[0] == str(issue):
                        url.append(issue_data[1])
                        break
                break
            break


    # Get links for each paper with progress bar
    for site in tqdm(url, desc="Getting paper links"):
        try:
            html_list = get_papers_link_aea(site, html_list, 30)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_aea(url_paper_list=html_list, paper_number=i, wait_time=30)
            if abstract:
                abstract_list.append(abstract)

                break
        except Exception as e:
            pass
    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)

def scrape_multiple_aea_journals(journal_list, volumes, issues):
    for journal_name in journal_list:
        print(f"Starting {journal_name}")
        scrape_aea_journal(journal_name, volumes, issues)

def main():
    volumes = [61]
    issues = [4]

    aea_journals = ['mac', 'aeri', 'pol', 'app', 'mic', 'jep']

    # scrape_aea_journal(journal_name='jel', volumes=volumes, issues=issues, get_link_dicts=False)
    scrape_multiple_aea_journals(aea_journals, volumes, issues)


if __name__ == "__main__":
    main()