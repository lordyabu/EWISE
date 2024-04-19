
# journal-web-scrapper

## Academic Journal Web Scraping Tool :newspaper: :computer:

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

A web scraping tool that extracts data from academic journals, including article titles, authors, and abstracts. :page_facing_up: :pencil2:

## Description :memo:

This tool is designed to fetch relevant information from academic journals and store the retrieved data in a structured format. By using web scraping techniques, it can efficiently gather article details, such as titles, authors, and abstracts, from various academic websites.

### Supported Journals in Economics

This tool currently supports a range of prestigious economic journals, including:

- Elsevier
- American Economic Journal
- Springer
- University of Chicago Press Journals
- Wiley
- Oxford University Press

## Features :rocket:

- Easily fetch article details from academic journals, with a focus on economics.
- Save the extracted data in a CSV or JSON format for further analysis.
- Customizable scraping options for different journal websites.
- Throttle mechanism to avoid overloading journal websites with requests.

## Getting Started

To run the tool, navigate to the `src/combined_runner.py` directory. Modify your preferences in the `main` function and execute the script (src/combined_runner.py) to start scraping the desired academic journals.

## Adding Support for New Journals

To add support for new journals already listed in `journal_website`, make sure to add the relevant information in the corresponding JSON file located in the `journal` sub-folder.

## To-Do

- Fix the `webscraper.webscrape_journal` function for streamlined import and use.
- Final Product should look like this 
```python
from journal-web-scrapper import webscrape_journal
```
