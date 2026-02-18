import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin
from datetime import datetime, timezone
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

# Select only article links
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

    # Remove leading date like 02/02/2026
    title = re.sub(r'^\d{2}/\d{2}/\d{4}', '', raw_title).strip()

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=full_url)

    # Add publication date (today, since site doesn't expose it cleanly)
    fe.pubDate(datetime.now(timezone.utc))

    count += 1
    if count >= 10:
        break

fg.rss_file("rss.xml")
