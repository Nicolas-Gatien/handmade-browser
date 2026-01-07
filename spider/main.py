import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
import nltk

def get_links(soup: BeautifulSoup, url: str):
    links = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href == "/":
            continue
        links.append(href)

    for i, link in enumerate(links):
        if "https://" in link:
            continue

        if link == "":
            continue

        origin = urlparse(url).hostname

        if link[0] == "/":
            links[i] = "https://" + origin + link
            continue

        links[i] =  "https://" + origin + '/' + link
    
    return links

def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_keywords(content: str):
    tokens = nltk.WhitespaceTokenizer().tokenize(content.lower())
    tagged = nltk.pos_tag(tokens)
    relevent_tags = []

    irrelevent_tags = ["DT", ":", "IN", "TO", "PRP", "JJ"]

    for tag in tagged:
        if tag[1] in irrelevent_tags:
            continue

        relevent_tags.append(tag[0])

    return relevent_tags

def write_files():
    with open('index.json', 'w') as file:
        file.write(json.dumps(index, indent=3))

    with open('queue.json', 'w') as file:
        file.write(json.dumps(queue, indent=3))

    with open('future.json', 'w') as file:
        file.write(json.dumps(future_places, indent=3))

    with open('reverse.json', 'w') as file:
        file.write(json.dumps(search_index, indent=3))


index = {}
queue = ["https://leylacornellportfolio.ca/", "https://nicolasgatien.com"]
future_places = {}
allowed_hostnames = []
search_index = {}

for start in queue:
    allowed_hostnames.append(urlparse(start).hostname)

while len(queue) > 0:
    url = urlparse(queue[0])
    hostname = url.hostname

    if hostname not in allowed_hostnames:
        print(hostname)
        future_places[hostname] = "found"
        queue.pop(0)
        continue

    if url.geturl() in index:
        queue.pop(0)
        continue

    #if input(f"\n{url.geturl()}:") == "s":
    #    queue.pop(0)
    #    continue

    soup = get_soup(url.geturl())
    links = get_links(soup, url.geturl())

    index[url.geturl()] = soup.get_text("\n")
    for link in links:
        queue.append(link)

    keywords = get_keywords(soup.get_text("\n"))
    for word in keywords:
        if word in search_index:
            if url.geturl() in search_index[word]:
                search_index[word][url.geturl()] += 1
            else:
                search_index[word][url.geturl()] = 1
        else:
            search_index[word] = {url.geturl(): 1}
    
    if (soup.title):
        title_keywords = get_keywords(soup.title.string)
        for word in title_keywords:
            if word in search_index:
                if url.geturl() in search_index[word]:
                    search_index[word][url.geturl()] += 5
                else:
                    search_index[word][url.geturl()] = 5
            else:
                search_index[word] = {url.geturl(): 5}


    write_files()
    
    queue.pop(0)

write_files()