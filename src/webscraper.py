from src.uchicago.uchicago_runner import automatic_scrape_uchicago_journal
from src.wiley.wiley_runner import automatic_scrape_wiley_journal
from src.oxford.oxford_runner import automatic_scrape_oxford_journal
from src.elsevier.elsevier_runner import automatic_scrape_elsevier_journal
from src.springer.springer_runner import automatic_scrape_springer_journal
from src.americanEconomicAssociation.aea_runner import automatic_scrape_aea_journal


def webscrape_journal(base_website, journal_name, num_prev_vols, wait_time):
    if base_website.lower() == "oxford":
        try:
            automatic_scrape_oxford_journal(journal_name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)
            print("Either 1. journal is not Oxford journal, 2. name inputted incorrectly, 3. journal not implemented")
    elif base_website.lower() == "wiley":
        try:
            automatic_scrape_wiley_journal(journal_name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)
            print("Either 1. journal is not Wiley journal, 2. name inputted incorrectly, 3. journal not implemented")
    elif base_website.lower() == "springer":
        try:
            automatic_scrape_springer_journal(journal_name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)
            print("Either 1. journal is not Springer journal, 2. name inputted incorrectly, 3. journal not implemented")
    elif base_website.lower() == "elsevier":
        try:
            automatic_scrape_elsevier_journal(journal_name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)
            print("Either 1. journal is not Elsevier journal, 2. name inputted incorrectly, 3. journal not implemented")
    elif base_website.lower() == "aea" or base_website.lower().replace(' ', '') == "americaneconomicjournal":
        try:
            automatic_scrape_aea_journal(journal_name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)
            print("Either 1. journal is not American Economic Association journal, 2. name inputted incorrectly, 3. journal not implemented")
    elif base_website.lower().replace(' ', '') == 'uchicago':
        try:
            automatic_scrape_uchicago_journal(journal_name, num_prev_vols, wait_time)
        except Exception as e:
            print(e)
            print("Either 1. journal is not Uchicago journal, 2. name inputted incorrectly, 3. journal not implemented")
    else:
        print(f"Base website {base_website} has been input correclty or has not been implemented yet")


def main():
        base_website = "aea"
        journal_name = "edcc"
        num_prev_vols = 1
        wait_time = 15

        webscrape_journal(base_website, journal_name, num_prev_vols, wait_time)

if __name__ == "__main__":
    main()