import requests
from bs4 import BeautifulSoup
from datetime import datetime
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

BASE_URL = "https://www.bbc.com"
NEWS_URL = "https://www.bbc.com/news"

def get_article_title(url):
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    return [title.get_text() for title in soup.find_all('title')]

def get_headlines_and_links(url):
    response = requests.get(url)

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


def summarize_text(text_input):
    summarizer = pipeline("summarization")
    return summarizer(text_input)[0]['summary_text']



if __name__ == "__main__":
    url = 'https://www.bbc.com/news/world-africa-65284945'

    # print(get_article_title("https://www.bbc.com/news/world-africa-65284945"))
    headlines_and_links = get_headlines_and_links("https://www.bbc.com/news")
    #articles = []

    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    title_embeddings = []

    article_to_check_title = get_article_title(url)[0]

    embedding1 = model.encode(article_to_check_title)

    index_to_title = {}

    for idx, (title, link) in enumerate(headlines_and_links):

        embedding2 = model.encode(title)

        index_to_title.update({idx: title})

        title_embeddings.append(embedding2)

    cosines = cosine_similarity(np.expand_dims(np.array(embedding1),axis=0), np.array(title_embeddings))[0]

    print(article_to_check_title,"IS SIMILAR TO", index_to_title[np.argmax(cosines)])

        # article = get_article_details(link)
        # if article:
        #    articles.append(article)
        #    print(f"Scraped: {article['headline']}")

# You can now analyze the content of the articles
# The 'articles' variable is a list of dictionaries containing the headline, link, publication_date, and content of each article

