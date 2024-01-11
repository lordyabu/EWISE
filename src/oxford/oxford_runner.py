from src.oxford.web_scraper_oxford import get_papers_link_oxford, get_abstract_info_oxford, get_latest_volume_number_oxford, \
    get_num_issues_oxford
from tqdm import tqdm
import json
import os.path
from config import USER_PATH, DATA_PATH


def scrape_multiple_oxford_journals(journal_list, num_prev_vols, wait_time):
    for name in journal_list:
        try:
            automatic_scrape_oxford_journal(name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)


def scrape_oxford_journal(name, automatic_collection, num_prev_vols, manual_vols=-1, manual_issues=-1, wait_time=15):
    if automatic_collection:
        automatic_scrape_oxford_journal(name, num_prev_vols, wait_time)
    else:
        manual_scrape_oxford_journals(name, manual_vols, manual_issues, wait_time)


def automatic_scrape_oxford_journal(name, num_prev_vols, wait_time):
    base_url = f"https://academic.oup.com/{name}"
    output_path = os.path.join(DATA_PATH, f'oxford_{name}.json')
    journal_url = "{}/issue/{{}}/{{}}".format(base_url)

    html_list = []
    abstract_list = []
    url = []

    num_issues = get_num_issues_oxford(name)

    # The Economic Journal does not reset issue # every volume
    if num_issues == "NY":
        raise ValueError("The Economic Journal is not supported yet")
        # issues = ['']
    else:
        issues = [i for i in range(1, num_issues + 1)]

    latest_vol = get_latest_volume_number_oxford(base_url, wait_time)
    starting_vol = max(1, latest_vol - num_prev_vols + 1)
    volumes = [vol for vol in range(starting_vol, latest_vol + 1)]

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
            html_list = get_papers_link_oxford(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_oxford(url_paper_list=html_list, paper_number=i, wait_time=wait_time)
            if abstract:
                abstract_list.append(abstract)
        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)


def manual_scrape_oxford_journals(name, volumes, issues, wait_time):

    if name == "ej":
        raise ValueError("The Economic Journal is not supported yet")

    base_url = f"https://academic.oup.com/{name}"
    output_path = os.path.join(DATA_PATH, f'oxford_{name}.json')
    journal_url = "{}/issue/{{}}/{{}}".format(base_url)

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
            html_list = get_papers_link_oxford(site, html_list, wait_time)
        except Exception as e:
            raise RuntimeError(f"Failed to get links for each paper: {e}")

    # Get Abstracts with progress bar
    for i in tqdm(range(len(html_list)), desc="Getting abstracts"):
        try:
            abstract = get_abstract_info_oxford(url_paper_list=html_list, paper_number=i, wait_time=wait_time)
            if abstract:
                abstract_list.append(abstract)
        except Exception as e:
            pass

    # Write data to JSON file
    with open(output_path, 'w') as json_file:
        json.dump(abstract_list, json_file)


def main():
    journal_list = ["restud", "rfs", "jeea", "wber", "jleo", "rof", "jcr", "ectj", "joeg", "rcfs", "oep", "jfec", "raps"]

    scrape_multiple_oxford_journals(journal_list, 1, 15)


if __name__ == "__main__":
    main()