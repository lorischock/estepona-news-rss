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

    # Remove leading date if present
    title = re.sub(r'^\d{2}/\d{2}/\d{4}', '', raw_title).strip()

    # Fetch article page to extract real publication date
    article_response = requests.get(full_url, headers=headers)
    article_soup = BeautifulSoup(article_response.text, "html.parser")

    date_tag = article_soup.select_one("#ContentNoticia_InfoBar li")

    if date_tag:
        date_text = date_tag.get_text(strip=True)
        try:
            pub_date = datetime.strptime(date_text, "%b %d, %Y at %I:%M %p")
            pub_date = pub_date.replace(tzinfo=timezone.utc)
        except:
            pub_date = datetime.now(timezone.utc)
    else:
        pub_date = datetime.now(timezone.utc)

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=full_url)
    fe.pubDate(pub_date)

    count += 1
    if count >= 20:
        break

fg.rss_file("rss.xml")
