from web_scraper_oxford import get_papers_link_oxford, get_abstract_info_oxford



volume = 75
issue = 1

url = f"https://academic.oup.com/oep/issue/{volume}/{issue}"


paper_links = get_papers_link_oxford(url, 15)



stuffs = get_abstract_info_oxford(paper_links, 0, 15)

print(stuffs)