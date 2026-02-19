import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin
from datetime import datetime, timezone, timedelta
import re

BASE_URL = "https://ayuntamiento.estepona.es"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Fetch homepage
response = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

fg = FeedGenerator()
fg.title("Ayuntamiento de Estepona - Noticias")
fg.link(href=BASE_URL)
fg.description("Últimas noticias del Ayuntamiento de Estepona")

articles = soup.select('a[href^="/noticia/"]')

seen = set()
article_data = []

# Collect article IDs + titles
for article in articles:
    href = article.get("href")
    if not href or href in seen:
        continue

    seen.add(href)

    match = re.search(r'/noticia/(\d+)', href)
    if not match:
        continue

    article_id = int(match.group(1))
    title = article.get_text(strip=True)

    if not title:
        continue

    full_url = urljoin(BASE_URL, href)
    article_data.append((article_id, title, full_url))

# Stop if nothing found
if not article_data:
    fg.rss_file("rss.xml")
    exit()

# Determine newest article ID
max_id = max(a[0] for a in article_data)

# Sort newest first
article_data.sort(reverse=True)

# Generate feed entries (TESTING MODE = 1 item)
for article_id, title, full_url in article_data[:1]:
    pub_date = datetime.now(timezone.utc) - timedelta(minutes=(max_id - article_id))

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=full_url)
    fe.guid(full_url, permalink=True)
    fe.pubDate(pub_date)

fg.rss_file("rss.xml")
