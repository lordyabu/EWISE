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
# Developed Modules

sys.path.append(os.path.join(USER_PATH, 'src'))
from src.helperFunctions.jsonHelpers import save_dict_as_json, load_json_as_dict
from src.jstor.web_scraper_jstor import get_papers_link_jstor, get_abstract_info_jstor, get_volume_and_issue_data_jstor, get_link_from_dict_jstor

# =============================================================================
# Parameters
# =============================================================================
#
# 1 - URL with the journal issue and volume as paramter
# journal_url = 'https://www.jstor.org/journal/jeconlite'
#
# url_links = get_volume_and_issue_data_jstor(journal_url)
#
# save_dict_as_json(url_links, 'jel.json')
#
# url_links_loaded = load_json_as_dict('jel.json')
# # 2 - Start empty list with link for each paper
# base_link = get_link_from_dict_jstor(url_links_loaded, 58, 2)
# print(base_link)
#
# html_list = []
#
# html_list = get_papers_link_jstor(base_link, html_list, 10)
# print(html_list)
#
# abstract_list = []
# try:
#     for i in range(1, len(html_list)):
#         abstract = get_abstract_info_jstor(url_paper_list=html_list, paper_number=i, wait_time=10)
#         abstract_list.append(abstract)
# except:
#     pass
#
# print(abstract_list)


def scrape_jstor_journal(journal_name, volumes, issues, get_link_dicts=True):
    """
    Scrapes information from Jstor journal webpages and saves it in a JSON file.

    This function automates the process of accessing Jstor journal webpages to collect
    detailed information about academic articles. It uses Selenium with GeckoDriver for
    web scraping. The information collected includes article titles, authors, abstracts,
    and issue/volume details. The progress of scraping is displayed using a progress bar.

    Args:
        journal_name (String): End of link for specific journal
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
    journal_url = f' https://www.jstor.org/journal/{journal_name}'

    output_path = os.path.join(DATA_PATH, f'jstor_{journal_name}.json')

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

    print(url)

    # Get links for each paper with progress bar
    for site in tqdm(url, desc="Getting paper links"):
        try:
            html_list = get_papers_link_jstor(site, html_list, 30)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    print(html_list, 'here')
    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_jstor(url_paper_list=html_list, paper_number=i, wait_time=30)
            if abstract:
                abstract_list.append(abstract)

            if i > 9:
                break
        except Exception as e:
            pass
    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)

#
# # =============================================================================
# # Application
# # =============================================================================
#
# # 1 - Generate strings for each volume and issue (choose either 1.1 or 1.2)
#
# ## 1.1 - With volume and issues
# try:
#     for volume in volumes:
#         for issue in issues:
#             url.append(journal_url.format(volume, issue))
# except:
#     pass
#
# ## 1.2 - With only volumes
# # try:
# #     for volume in volumes:
# #         url.append(journal_url.format(volume))
# # except:
# #     pass
#
# ## 2 - Get links for each paper
# try:
#     for site in url:
#         html_list = get_papers_link(site, html_list, 5)
# except:
#     pass
#
# print(html_list)
#
# # 3 - Get Abstracts from step 2
# try:
#     for i in range(1, len(html_list)):
#         abstract = get_abstract_info(url_paper_list=html_list, paper_number=i, wait_time=10, title_id=title_id,
#                                      author_id=author_id, abstract_id=abstract_id, issue_vol_id=issue_vol_id)
#         abstract_list.append(abstract)
# except:
#     pass

# =============================================================================
# =============================================================================


def main():
    volumes = [58]
    issues = [4]

    scrape_jstor_journal(journal_name='jeconlite', volumes=volumes, issues=issues)


if __name__ == "__main__":
    main()