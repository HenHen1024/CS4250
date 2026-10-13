
#-------------------------------------------------------------------------
# AUTHOR: Henry He
# FILENAME: scraper.py
# SPECIFICATION: Crawl the Circular Links section of TestingURL.dev
# FOR: CS 4250 - Assignment #2
# TIME SPENT: about 2.5-3 hours for the scraper.
#-------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse

# Defining the seed URL
seed = "https://testingurl.dev/scraping/links/circular"
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
    for a_tag in soup.find_all("a", href=True):
        link = a_tag["href"].strip()
        current = urlparse(url)

        # Convert relative URLs to absolute URLs without urljoin()
        if link.startswith("https://") or link.startswith("http://"):
            absolute_url = link
        elif link.startswith("//"):
            absolute_url = current.scheme + ":" + link
        elif link.startswith("/"):
            absolute_url = current.scheme + "://" + current.netloc + link
        elif link.startswith("#"):
            absolute_url = urlunparse(
                (current.scheme, current.netloc, current.path,
                 current.params, current.query, link[1:])
            )
        elif link.startswith("?"):
            absolute_url = urlunparse(
                (current.scheme, current.netloc, current.path,
                 current.params, link[1:], "")
            )
        else:
            # Resolve relative paths, including "." and ".."
            path_parts = current.path.split("/")
            if path_parts:
                path_parts.pop()

            for part in link.split("/"):
                if part in ("", "."):
                    continue
                if part == "..":
                    if path_parts:
                        path_parts.pop()
                else:
                    path_parts.append(part)

            new_path = "/" + "/".join(path_parts)
            absolute_url = urlunparse(
                (current.scheme, current.netloc, new_path, "", "", "")
            )

        # Follow only URLs in the required section or its subpaths
        if (absolute_url == allowed_prefix or
                absolute_url.startswith(allowed_prefix + "/")):
            if absolute_url not in seen:
                seen.add(absolute_url)
                frontier.append(absolute_url)

# Printing all URLs in seen
for seen_url in seen:
    print(seen_url)
