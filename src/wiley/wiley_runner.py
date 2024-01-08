from web_scrapper_wiley import get_paper_number_from_name, get_papers_link_wiley, get_abstract_info_wiley


int_paper = get_paper_number_from_name('The Journal of Finance')

volume = 78
issue = 4


url = f"https://onlinelibrary.wiley.com/toc/{int_paper}/{volume}/{issue}"


paper_links = get_papers_link_wiley(url, 15)

stuffs = get_abstract_info_wiley(paper_links, 2, 15)

print(stuffs)