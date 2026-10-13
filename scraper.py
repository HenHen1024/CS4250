
#-------------------------------------------------------------------------
# AUTHOR: Henry He
# FILENAME: scraper.py
# SPECIFICATION: Crawl the Circular Links section of TestingURL.dev
# FOR: CS 4250 - Assignment #2
# TIME SPENT: about 2.5-3 hours for the scraper.
#-------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Defining the seed URL
seed = "https://testingurl.dev/scraping/links/circular"
baseURL = "https://testingurl.dev"
allowed_prefix = "https://testingurl.dev/scraping/links/circular"

# Creating the frontier and seen collections
frontier = [seed]
seen = {seed}

# Crawling until the frontier is empty
while frontier:

    # Removing the first URL from the frontier
    url = frontier.pop(0)

    # Retrieving and parsing the Web page
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Printing the text contained in the <h1> element
    h1 = soup.find("h1")
    if h1 is not None:
        print(h1.get_text(strip=True))

    # Extracting and processing hyperlinks
    links = []
    for a_tag in soup.find_all("a", href=True):
        absolute_url = urljoin(url, a_tag["href"])

        if absolute_url.startswith(allowed_prefix):
            links.append(absolute_url)

    # Add unseen links to seen and the frontier
    for link in links:
        if link not in seen:
            seen.add(link)
            frontier.append(link)

# Printing all URLs in seen
for url in seen:
    print(url)
