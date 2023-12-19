from src.elsevier.elsevier_runner import scrape_multiple_elsevier_journals
from src.econometrica.econometrica_runner import scrape_econometrica_journal
from src.americanEconomicAssociation.aea_runner import scrape_multiple_aea_journals

def main():
    run_elsevier = True
    run_econometrica = False
    run_aea = False

    if run_elsevier:
        journal_list = ["journal-of-empirical-finance", 'journal-of-economic-behavior-and-organization',
                        'journal-of-economic-dynamics-and-control', 'journal-of-economic-theory',
                        'journal-of-environmental-economics-and-management', 'journal-of-health-economics',
                        'journal-of-international-economics', 'journal-of-international-money-and-finance',
                        'journal-of-mathematical-economics', 'journal-of-monetary-economics',
                        'journal-of-public-economics',
                        'journal-of-econometrics', 'journal-of-development-economics', 'asia-and-the-global-economy',
                        'journal-of-accounting-and-economics', 'journal-of-financial-markets',
                        'journal-of-macroeconomics',
                        'journal-of-economics-and-business', 'journal-of-financial-economics', 'economic-modelling']
        volumes = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
        issues = [0]
        title_id = 'screen-reader-main-title'
        author_id = 'author-group'
        abstract_id = 'abstracts'
        issue_vol_id = 'publication-title'
        metric_id = 'metrics-header'
        keyword_id = 'keys0001'

        scrape_multiple_elsevier_journals(journal_list=journal_list, volumes=volumes, issues=issues, title_id=title_id,
                                          author_id=author_id, abstract_id=abstract_id, issue_vol_id=issue_vol_id,
                                          metric_id=metric_id, keyword_id=keyword_id)

    if run_econometrica:
        volumes = [91]
        issues = [6]

        scrape_econometrica_journal(volumes=volumes, issues=issues)


    if run_aea:
        volumes = [61]
        issues = [4]

        aea_journals = ['mac', 'aeri', 'pol', 'app', 'mic', 'jep']
        scrape_multiple_aea_journals(aea_journals, volumes, issues)


if __name__ == "__main__":
    main()