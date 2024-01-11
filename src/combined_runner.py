# -*- coding: utf-8 -*-

"""
Main Runner for Academic Journal Web Scrapers

This script is designed to execute web scraping tasks for various academic journals.
It leverages specific scraping modules for journals from Elsevier, Econometrica,
the American Economic Association (AEA), and the University of Chicago. Each module
is equipped to extract article details such as titles, authors, abstracts, and more,
using Selenium and appropriate web drivers.

The script allows selective execution of scraping tasks based on predefined flags.

Modules:
    scrape_multiple_elsevier_journals: Handles scraping of multiple journals from Elsevier.
    scrape_multiple_aea_journals: Handles scraping of multiple journals from the AEA.
    scrape_uchicago_journal: Handles scraping of a journal from the University of Chicago.

Usage:
    Set the respective flags for Elsevier, Econometrica, AEA, and UChicago journals to True to enable scraping.
    Configure the volume and issue numbers for each set of journals to scrape.
    Run this script to initiate the scraping process for the enabled journals.
"""

from src.elsevier.elsevier_runner import scrape_multiple_elsevier_journals
from src.uchicago.uchicago_runner import scrape_multiple_uchicago_journals
from src.americanEconomicAssociation.aea_runner import scrape_multiple_aea_journals
from src.oxford.oxford_runner import scrape_multiple_oxford_journals
from src.springer.springer_runner import scrape_multiple_springer_journals
from src.wiley.wiley_runner import scrape_multiple_wiley_journals
def main():
    run_elsevier = True
    run_aea = False
    run_uchicago = False
    run_oxford = False
    run_springer = False
    run_wiley = False

    num_prev_vols = 1

    elsevier_wait_time = 15
    aea_wait_time = 30
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

        scrape_multiple_elsevier_journals(journal_list=elsevier_journals, num_prev_vols=num_prev_vols, wait_time=elsevier_wait_time)



    if run_aea:
        aea_journals = ['jel', 'mac', 'aeri', 'pol', 'app', 'mic', 'jep', 'aer']
        scrape_multiple_aea_journals(journal_list=aea_journals, num_prev_vols=num_prev_vols, wait_time=aea_wait_time)

    if run_uchicago:
        uchicago_journals = ['edcc', 'jole', 'jle', 'jpe', 'ntj', 'reep']

        scrape_multiple_uchicago_journals(journal_list=uchicago_journals, num_prev_vols=num_prev_vols, wait_time=uchicago_wait_time)

    if run_oxford:
        oxford_journals = ["restud", "rfs", "jeea", "wber", "jleo", "rof", "jcr", "ectj", "joeg", "rcfs", "oep", "jfec",
                        "raps"]

        scrape_multiple_oxford_journals(journal_list=oxford_journals, num_prev_vols=num_prev_vols, wait_time=oxford_wait_time)


    if run_springer:
        springer_journals = ['IMF Economic Review', 'Journal of Economic Growth', 'Journal of Risk and Uncertainty',
                        'Journal of Population Economics', 'Economic Theory', 'Public Choice', 'Empirical Economics']

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

        scrape_multiple_wiley_journals(journal_list=wiley_journals, num_prev_vols=num_prev_vols, wait_time=wiley_wait_time)



if __name__ == "__main__":
    main()