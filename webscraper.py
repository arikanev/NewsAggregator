import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://www.bbc.com"
NEWS_URL = "https://www.bbc.com/news"

def get_headlines_and_links():
    response = requests.get(NEWS_URL)

    if response.status_code != 200:
        print(f"Failed to fetch the BBC News website. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    headlines_and_links = []

    for headline in soup.find_all("a", class_="gs-c-promo-heading"):
        title = headline.text.strip()
        link = headline["href"]
        if not link.startswith("http"):
            link = BASE_URL + link
        headlines_and_links.append((title, link))

    return headlines_and_links

def get_article_details(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the article URL ({url}). Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text.strip()

    date = soup.find("time", {"data-testid": "timestamp"})
    if date:
        date = date.text.strip()
        try:
            date = datetime.strptime(date, "%d %B %Y")
        except ValueError:
            date = "Date not found"
    else:
        date = "Date not found"

    content = []
    body = soup.find("article")
    if body:
        for paragraph in body.find_all("p"):
            content.append(paragraph.text.strip())

    return {
        "headline": title,
        "link": url,
        "publication_date": date,
        "content": " ".join(content),
    }

if __name__ == "__main__":
    headlines_and_links = get_headlines_and_links()

    articles = []
    for title, link in headlines_and_links:
        article = get_article_details(link)
        if article:
            articles.append(article)
            print(f"Scraped: {article['headline']}")

# You can now analyze the content of the articles
# The 'articles' variable is a list of dictionaries containing the headline, link, publication_date, and content of each article

