import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

URL = "https://www.estepona.es/actualidad/"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

fg = FeedGenerator()
fg.title("Estepona News")
fg.link(href=URL)
fg.description("Latest news from Ayuntamiento de Estepona")

articles = soup.select("h2 a")

for article in articles[:10]:
    fe = fg.add_entry()
    fe.title(article.get_text(strip=True))
    fe.link(href=article["href"])

fg.rss_file("rss.xml")
