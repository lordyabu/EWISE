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
    scrape_econometrica_journal: Handles scraping of journals from Econometrica.
    scrape_multiple_aea_journals: Handles scraping of multiple journals from the AEA.
    scrape_uchicago_journal: Handles scraping of a journal from the University of Chicago.

Usage:
    Set the respective flags for Elsevier, Econometrica, AEA, and UChicago journals to True to enable scraping.
    Configure the volume and issue numbers for each set of journals to scrape.
    Run this script to initiate the scraping process for the enabled journals.
"""

from src.elsevier.elsevier_runner import scrape_multiple_elsevier_journals
from src.econometrica.econometrica_runner import scrape_econometrica_journal
from src.americanEconomicAssociation.aea_runner import scrape_multiple_aea_journals
from src.uchicago.uchicago_runner import scrape_multiple_uchicago_journals
def main():
    run_jstor = False
    run_elsevier = False
    run_econometrica = False
    run_aea = False
    run_uchicago = True


    if run_jstor:
        journal_list = ['jeconlite']

        volumes = [58]
        issues = [4]

    if run_elsevier:
        #ToDo: Most likely need to manually get vol/issues for each journal
        journal_list = ['journal-of-empirical-finance', 'journal-of-economic-behavior-and-organization',
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
                        'european-journal-of-political-economy']
        volumes = [60]
        issues = [0]

        scrape_multiple_elsevier_journals(journal_list=journal_list, volumes=volumes, issues=issues)

    if run_econometrica:
        #ToDo: Most likely need to manually get vol/issues for each journal
        volumes = [91]
        issues = [5, 6]

        scrape_econometrica_journal(volumes=volumes, issues=issues)


    if run_aea:
        #ToDo: Can modify scrape_aea_journal() to use last X volumes
        volumes = [61]
        issues = [4]

        aea_journals = ['mac', 'aeri', 'pol', 'app', 'mic', 'jep']
        scrape_multiple_aea_journals(aea_journals, volumes, issues)

    if run_uchicago:
        #ToDo: Most likely need to manually get vol/issues for each journal
        volumes = [131]
        issues = [11]

        uchicago_journals = ['edcc', 'jole', 'jle', 'jpe', 'ntj', 'reep']

        scrape_multiple_elsevier_journals(journal_list=uchicago_journals, volumes=volumes, issues=issues)

    #ToDo: Figure out how to get past jstor detection system


if __name__ == "__main__":
    main()