import requests
from bs4 import BeautifulSoup

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

if __name__ == "__main__":
    headlines_and_links = get_headlines_and_links()
    for title, link in headlines_and_links:
        print(f"{title}\n{link}\n")
