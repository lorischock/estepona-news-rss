import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin

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

# Select news article links
articles = soup.select('a[href^="/noticia/"]')

seen = set()

for article in articles:
    href = article.get("href")

    if not href or href in seen:
        continue

    seen.add(href)

    full_url = urljoin(BASE_URL, href)
    title = article.get_text(strip=True)

    if not title:
        continue

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=full_url)

fg.rss_file("rss.xml")
