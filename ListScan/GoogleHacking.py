import requests
from urllib.parse import urlparse

SEARCH_ENGINE_ID = ""
API_KEY = ""

search_keyword = ""
search_filetype = ""
targets = []
with open('links.txt', 'r') as file:
    links = file.readlines()
    targets = [urlparse(link).netloc for link in links]

for target in targets:
    search_query = f"site:{target} {search_keyword}"
    response = requests.get(f"https://www.googleapis.com/customsearch/v1?cx={SEARCH_ENGINE_ID}&key={API_KEY}&q={search_query}&fileType={search_filetype}")
    data = response.json()

    for item in data['items']:
        print(f"========== Link: {item['link']} ==========")
        print(f"Title: {item['title']}")
        print(f"Snippet: {item['snippet']}")
        print(f"\n")