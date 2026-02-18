import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin

URL = "https://www.estepona.es/actualidad/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

fg = FeedGenerator()
fg.title("Estepona News")
fg.link(href=URL)
fg.description("Latest news from Ayuntamiento de Estepona")

articles = soup.select("h2 a")

for article in articles:
    href = article.get("href")

    if not href:
        continue

    full_url = urljoin(URL, href)

    fe = fg.add_entry()
    fe.title(article.get_text(strip=True))
    fe.link(href=full_url)

fg.rss_file("rss.xml")
