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
from config import USER_PATH

# Developed Modules

sys.path.append(os.path.join(USER_PATH, 'src'))
from src.elsevier.web_scrapper_elsevier import get_papers_link, get_abstract_info

# =============================================================================
# Parameters
# =============================================================================

# 1 - URL with the journal issue and volume as paramter
journal_url = 'https://www.sciencedirect.com/journal/journal-of-macroeconomics/vol/{}/suppl/C'

# 2 - Start empty list with link for each paper
html_list = []
abstract_list = []

# 3 - Issues and Volumes availables
volumes = [67]
# issues = [1,2,3,4]
issues = [1, 2]
url = []

# 4 - HTML Div IDs
title_id = 'screen-reader-main-title'
author_id = 'author-group'
abstract_id = 'abstracts'
issue_vol_id = 'publication-title'

# =============================================================================
# Application
# =============================================================================

# 1 - Generate strings for each volume and issue (choose either 1.1 or 1.2)

## 1.1 - With volume and issues
try:
    for volume in volumes:
        for issue in issues:
            url.append(journal_url.format(volume, issue))
except:
    pass

## 1.2 - With only volumes
try:
    for volume in volumes:
        url.append(journal_url.format(volume))
except:
    pass

## 2 - Get links for each paper
try:
    for site in url:
        html_list = get_papers_link(site, html_list, 5)
except:
    pass

# 3 - Get Abstracts from step 2
try:
    for i in range(1, len(html_list)):
        abstract = get_abstract_info(url_paper_list=html_list, paper_number=i, wait_time=10, title_id=title_id,
                                     author_id=author_id, abstract_id=abstract_id, issue_vol_id=issue_vol_id)
        abstract_list.append(abstract)
except:
    pass

# =============================================================================
# =============================================================================
