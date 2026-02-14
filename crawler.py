import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

START_URL = "https://www.bbc.com/news"
BASE_DOMAIN = "www.bbc.com"
MAX_PAGES = 100

visited = set()
to_visit = [START_URL]

if not os.path.exists("pages"):
    os.makedirs("pages")

index_file = open("index.txt", "w", encoding="utf-8")

page_count = 0

headers = {
    "User-Agent": "Mozilla/5.0"
}

while to_visit and page_count < MAX_PAGES:
    url = to_visit.pop(0)

    if url in visited:
        continue

    try:
        print(f"Downloading: {url}")
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            continue

        html = response.text

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()

        if len(text.strip()) < 1000:
            continue  

        page_count += 1
        filename = f"pages/{page_count}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)

        index_file.write(f"{page_count} - {url}\n")

        visited.add(url)

        for link in soup.find_all("a", href=True):
            href = link["href"]
            full_url = urljoin(url, href)

            parsed = urlparse(full_url)

            if parsed.netloc == BASE_DOMAIN and full_url.startswith("http"):
                if full_url not in visited:
                    to_visit.append(full_url)

        time.sleep(1)

    except Exception as e:
        print(f"Error con {url}: {e}")

index_file.close()

print("Download Complete!")
