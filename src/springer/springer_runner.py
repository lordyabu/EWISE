from src.springer.web_scraper_springer import get_latest_volume_number_springer, get_num_issues_springer, get_paper_number_from_name_springer, get_papers_link_springer, get_abstract_info_springer
from tqdm import tqdm
import json
import os.path
from config import USER_PATH, DATA_PATH


def scrape_multiple_springer_journals(journal_list, num_prev_vols, wait_time):
    for name in journal_list:
        try:
            automatic_scrape_springer_journal(name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)


def scrape_springer_journal(name, automatic_collection, num_prev_vols, manual_vols=-1, manual_issues=-1, wait_time=15):
    if automatic_collection:
        automatic_scrape_springer_journal(name, num_prev_vols, wait_time)
    else:
        manual_scrape_springer_journals(name, manual_vols, manual_issues, wait_time)


def automatic_scrape_springer_journal(name, num_prev_vols, wait_time):
    int_paper = get_paper_number_from_name_springer(name)
    volume_url = f"https://link.springer.com/journal/{int_paper}/volumes-and-issues"
    journal_url = "https://link.springer.com/journal/{}/volumes-and-issues/{{}}-{{}}".format(int_paper)
    output_path = os.path.join(DATA_PATH, f'springer_{name}.json')

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
            abstract = get_abstract_info_springer(url_paper_list=html_list, paper_number=i, wait_time=wait_time)
            if abstract:
                abstract_list.append(abstract)
        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)


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


def main():
    journal_list = ['IMF Economic Review', 'Journal of Economic Growth', 'Journal of Risk and Uncertainty', 'Journal of Population Economics', 'Economic Theory', 'Public Choice', 'Empirical Economics']
    scrape_multiple_springer_journals(journal_list, 1, 15)

if __name__ == "__main__":
    main()