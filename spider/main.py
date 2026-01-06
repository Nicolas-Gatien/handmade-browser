import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json

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

index = {}
queue = ["https://nicolasgatien.com"]
future_places = {}
allowed_hostnames = []

for start in queue:
    allowed_hostnames.append(urlparse(start).hostname)

while len(queue) > 0:
    url = urlparse(queue[0])
    hostname = url.hostname

    #print(hostname, allowed_hostnames)

    if hostname not in allowed_hostnames:
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

    index[url.geturl()] = soup.get_text()
    for link in links:
        queue.append(link)

    for link in links:
        print(link)

    print()

    with open('index.json', 'w') as file:
        file.write(json.dumps(index, indent=3))

    with open('queue.json', 'w') as file:
        file.write(json.dumps(queue, indent=3))

    with open('future.json', 'w') as file:
        file.write(json.dumps(future_places, indent=3))

    queue.pop(0)



