# -*- coding: utf-8 -*-

"""
Main Runner for Academic Journal Web Scrapers

This script is designed to facilitate web scraping tasks for a wide range of academic journals from multiple publishers including Elsevier, Econometrica, the American Economic Association (AEA), the University of Chicago, Oxford, Springer, and Wiley. Each module within the script is tailored to scrape specific journals from these publishers, extracting article details like titles, authors, abstracts, and more, utilizing Selenium and appropriate web drivers.

The script is flexible, allowing selective execution of scraping tasks for different journals from various publishers. This is managed through predefined flags that can be set for each publisher's set of journals.

Modules:
    scrape_multiple_elsevier_journals: Handles scraping of multiple journals from Elsevier.
    scrape_multiple_aea_journals: Handles scraping of multiple journals from the AEA.
    scrape_multiple_uchicago_journals: Handles scraping of multiple journals from the University of Chicago.
    scrape_multiple_oxford_journals: Handles scraping of multiple journals from Oxford.
    scrape_multiple_springer_journals: Handles scraping of multiple journals from Springer.
    scrape_multiple_wiley_journals: Handles scraping of multiple journals from Wiley.

Usage:
    Set the respective flags for Elsevier, AEA, UChicago, Oxford, Springer, and Wiley journals to True to enable their scraping.
    Configure the # of previous volumes wanted
    Run this script to initiate the scraping process for the enabled journals.

Note:
    The wait times and the number of previous volumes to scrape can be adjusted for each publisher's set of journals.
"""


from src.elsevier.elsevier_runner import scrape_multiple_elsevier_journals
from src.uchicago.uchicago_runner import scrape_multiple_uchicago_journals
from src.americanEconomicAssociation.aea_runner import scrape_multiple_aea_journals
from src.oxford.oxford_runner import scrape_multiple_oxford_journals
from src.springer.springer_runner import scrape_multiple_springer_journals
from src.wiley.wiley_runner import scrape_multiple_wiley_journals
def main():
    run_elsevier = True
    run_aea = True
    run_uchicago = True
    run_oxford = True
    run_springer = True
    run_wiley = False

    num_prev_vols = 1

    elsevier_wait_time = 15
    aea_wait_time = 15
    uchicago_wait_time = 15
    oxford_wait_time = 15
    springer_wait_time = 15
    wiley_wait_time = 15




    if run_elsevier:
        elsevier_journals = ['journal-of-empirical-finance', 'journal-of-economic-behavior-and-organization',
                        'journal-of-economic-dynamics-and-control', 'journal-of-economic-theory',
                        'journal-of-environmental-economics-and-management', 'journal-of-health-economics',
                        'journal-of-international-economics', 'journal-of-international-money-and-finance',
                        'journal-of-mathematical-economics', 'journal-of-monetary-economics',
                        'journal-of-public-economics',
                        'journal-of-econometrics', 'journal-of-development-economics', 'asia-and-the-global-economy',
                        'journal-of-accounting-and-economics', 'journal-of-financial-markets',
                        'journal-of-macroeconomics',
                        'journal-of-economics-and-business', 'journal-of-financial-economics', 'economic-modelling',
                        'economia', 'energy-policy', 'journal-of-financial-intermediation', 'european-economic-review',
                        'review-of-economic-dynamics', 'journal-of-banking-and-finance', 'energy-economics',
                        'journal-of-urban-economics', 'games-and-economic-behavior', 'world-development',
                        'economics-letters', 'labour-economics', 'journal-of-corporate-finance', 'ecological-economics',
                        'european-journal-of-political-economy', 'international-economics',
                        'economics-of-education-review',
                        'international-journal-of-forecasting']

        # elsevier_journals = ['journal-of-empirical-finance']

        scrape_multiple_elsevier_journals(journal_list=elsevier_journals, num_prev_vols=num_prev_vols, wait_time=elsevier_wait_time)



    if run_aea:
        aea_journals = ['jel', 'mac', 'aeri', 'pol', 'app', 'mic', 'jep', 'aer']

        # aea_journals = ['jel']

        scrape_multiple_aea_journals(journal_list=aea_journals, num_prev_vols=num_prev_vols, wait_time=aea_wait_time)

    if run_uchicago:
        uchicago_journals = ['edcc', 'jole', 'jle', 'jpe', 'ntj', 'reep']

        # uchicago_journals = ['jole']


        scrape_multiple_uchicago_journals(journal_list=uchicago_journals, num_prev_vols=num_prev_vols, wait_time=uchicago_wait_time)

    if run_oxford:
        oxford_journals = ["restud", "rfs", "jeea", "wber", "jleo", "rof", "jcr", "ectj", "joeg", "rcfs", "oep", "jfec",
                        "raps"]

        # oxford_journals = ['restud']

        scrape_multiple_oxford_journals(journal_list=oxford_journals, num_prev_vols=num_prev_vols, wait_time=oxford_wait_time)


    if run_springer:
        springer_journals = ['IMF Economic Review', 'Journal of Economic Growth', 'Journal of Risk and Uncertainty',
                        'Journal of Population Economics', 'Economic Theory', 'Public Choice', 'Empirical Economics']

        # springer_journals = ['IMF Economic Review']

        scrape_multiple_springer_journals(journal_list=springer_journals, num_prev_vols=num_prev_vols, wait_time=springer_wait_time)

    if run_wiley:
        wiley_journals = ['The Journal of Finance',
                        'Journal of Money, Credit and Banking',
                        'RAND Journal of Economics',
                        'Journal of Applied Econometrics',
                        'International Economic Review',
                        'Oxford Bulletin of Economics and Statistics',
                        'Journal of Economic Surveys',
                        'Journal of Accounting Research',
                        'Quantitative Economics',
                        'Journal of Industrial Economics',
                        'Scandinavian Journal of Economics',
                        'Journal of Economics & Management Strategy',
                        'Theoretical Economics',
                        'Economic Enquiry',
                        'American Journal of Agricultural Economics',
                        'Economics and Politics',
                        'Canadian Journal of Economics',
                        'Journal of Forecasting']

        # wiley_journals = ['The Journal of Finance']

        scrape_multiple_wiley_journals(journal_list=wiley_journals, num_prev_vols=num_prev_vols, wait_time=wiley_wait_time)



if __name__ == "__main__":
    main()