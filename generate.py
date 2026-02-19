articles = soup.select('a[href^="/noticia/"]')

seen = set()
count = 0
article_data = []

# First collect all article IDs
for article in articles:
    href = article.get("href")
    if not href or href in seen:
        continue

    seen.add(href)

    match = re.search(r'/noticia/(\d+)', href)
    if not match:
        continue

    article_id = int(match.group(1))
    raw_title = article.get_text(strip=True)
    if not raw_title:
        continue

    full_url = urljoin(BASE_URL, href)
    article_data.append((article_id, raw_title.strip(), full_url))

# Determine newest ID
if not article_data:
    fg.rss_file("rss.xml")
    exit()

max_id = max(a[0] for a in article_data)

# Now create feed entries
for article_id, title, full_url in article_data:
    pub_date = datetime.now(timezone.utc) - timedelta(minutes=(max_id - article_id))

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=full_url)
    fe.pubDate(pub_date)
    fe.guid(full_url, permalink=True)

    count += 1
    if count >= 20:
        break
