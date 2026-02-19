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

response = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

fg = FeedGenerator()
fg.title("Ayuntamiento de Estepona - Noticias")
fg.link(href=BASE_URL)
fg.description("Últimas noticias del Ayuntamiento de Estepona")

articles = soup.select('a[href^="/noticia/"]')

seen = set()
count = 0

for article in articles:
    href = article.get("href")

    if not href or href in seen:
        continue

    seen.add(href)

    full_url = urljoin(BASE_URL, href)
    raw_title = article.get_text(strip=True)

    if not raw_title:
        continue

    title = raw_title.strip()

    # Extract numeric article ID
    match = re.search(r'/noticia/(\d+)', href)
    if not match:
        continue

    article_id = int(match.group(1))

    # Create stable pseudo-date based on article ID
    base_date = datetime(2020, 1, 1, tzinfo=timezone.utc)
    pub_date = base_date + timedelta(minutes=article_id)

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=full_url)
    fe.pubDate(pub_date)
    fe.guid(full_url, permalink=True)

    count += 1
    if count >= 20:
        break

fg.rss_file("rss.xml")
