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
def scrape_elsevier_journal(journal_name, volumes, issues, title_id, author_id, abstract_id, issue_vol_id, metric_id, keyword_id):
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
            abstract = get_abstract_info_elsevier(url_paper_list=html_list, paper_number=i, wait_time=3, title_id=title_id,
                                         author_id=author_id, abstract_id=abstract_id, issue_vol_id=issue_vol_id)
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
def scrape_multiple_elsevier_journals(journal_list, volumes, issues, title_id, author_id, abstract_id, issue_vol_id, metric_id, keyword_id):
    for journal_name in journal_list:
        print(f"Starting {journal_name}")
        scrape_elsevier_journal(journal_name, volumes, issues, title_id, author_id, abstract_id, issue_vol_id, metric_id, keyword_id)


# =============================================================================
# Main
# =============================================================================
def main():
    journal_list = ["journal-of-empirical-finance", 'journal-of-economic-behavior-and-organization', 'journal-of-economic-dynamics-and-control', 'journal-of-economic-theory', 'journal-of-environmental-economics-and-management', 'journal-of-health-economics', 'journal-of-international-economics', 'journal-of-international-money-and-finance', 'journal-of-mathematical-economics', 'journal-of-monetary-economics', 'journal-of-public-economics', 'journal-of-econometrics', 'journal-of-development-economics', 'asia-and-the-global-economy', 'journal-of-accounting-and-economics', 'journal-of-financial-markets', 'journal-of-macroeconomics', 'journal-of-economics-and-business', 'journal-of-financial-economics', 'economic-modelling']
    volumes = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
    issues = [0]
    title_id = 'screen-reader-main-title'
    author_id = 'author-group'
    abstract_id = 'abstracts'
    issue_vol_id = 'publication-title'
    metric_id = 'metrics-header'
    keyword_id = 'keys0001'

    scrape_multiple_elsevier_journals(journal_list=journal_list, volumes=volumes, issues=issues, title_id=title_id,
                            author_id=author_id, abstract_id=abstract_id, issue_vol_id=issue_vol_id, metric_id=metric_id, keyword_id=keyword_id)


if __name__ == "__main__":
    main()