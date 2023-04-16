import requests
from bs4 import BeautifulSoup
from datetime import datetime
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import pandas as pd
import re 
import openai

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import classification_report
import time

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


# Text preprocessing
def preprocess(text):
    
    """
    Function: split text into words and return the root form of the words
    Args:
      text(str): the article
    Return:
      lem(list of str): a list of the root form of the article words
    """
        
    # Normalize text
    text = re.sub(r"[^a-zA-Z]", " ", str(text).lower())
    
    # Tokenize text
    token = word_tokenize(text)
    
    # Remove stop words
    stop = stopwords.words("english")
    words = [t for t in token if t not in stop]
    
    # Lemmatization
    lem = [WordNetLemmatizer().lemmatize(w) for w in words]
    
    return lem

def fit_eval_model(model, train_features, y_train, test_features, y_test):
    
    """
    Function: train and evaluate a machine learning classifier.
    Args:
      model: machine learning classifier
      train_features: train data extracted features
      y_train: train data lables
      test_features: train data extracted features
      y_test: train data lables
    Return:
      results(dictionary): a dictionary of the model training time and classification report
    """
    results ={}
    
    # Start time
    start = time.time()
    # Train the model
    model.fit(train_features, y_train)
    # End time
    end = time.time()
    # Calculate the training time
    results['train_time'] = end - start
    
    # Test the model
    test_predicted = model.predict(test_features)
    
     # Classification report
    results['classification_report'] = classification_report(y_test, test_predicted)
        
    return results

# Classify an article
def classify_article(tf_vec, nb, content):
    
    """
    Function: classify an article.
    Args:
      path: the path of the article 
    Return:
      category (str): the category of the article
    """

    # Text preprocessing
    artcl = preprocess(content)
    artcl = ' '.join(artcl)

    # Use TF_IDF
    test = tf_vec.transform([artcl])

    # Use MultinomialNB model to classify the article
    predict = nb.predict(test)
    category = predict[0]

    return category

def run_GPT4(string):
    openai.api_key = ""


    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": "Summarize: " + string}
        ]
    )
    output = completion.choices[0].message
    return output['content']


def run(url):
    url = 'https://www.bbc.com/news/world-africa-65284945'

    # print(get_article_title("https://www.bbc.com/news/world-africa-65284945"))
    headlines_and_links = get_headlines_and_links("https://www.bbc.com/news")
    #articles = []

    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    title_embeddings = []

    article_to_check_title = get_article_title(url)[0]

    embedding1 = model.encode(article_to_check_title)

    index_to_title = {}

    index_to_article = {}

    articles = []

    for idx, (title, link) in enumerate(headlines_and_links):

        embedding2 = model.encode(title)

        index_to_title.update({idx: title})

        title_embeddings.append(embedding2)

        article = get_article_details(link)

        article_dict = {}

        if article:
            article_dict.update({"title":title, "content":article['content']})
            articles.append(article_dict)
            index_to_article.update({idx: article['content']})

    cosines = cosine_similarity(np.expand_dims(np.array(embedding1),axis=0), np.array(title_embeddings))[0]

    similar_article_indices = np.argpartition(cosines, -3)[-3:]

    print(article_to_check_title,"IS SIMILAR TO", [index_to_title[i] for i in similar_article_indices])

    json_obj = json.dumps(articles)
    # print(json_obj)

    df1 = pd.read_csv('BBC News Train.csv')
    category = list(df1['Category'].unique())
    print(category)

    df1["Preprocessed_Text"] = df1['Text'].apply(lambda x: preprocess(x))
    df1['Preprocessed_Text2'] = df1['Preprocessed_Text'].apply(' '.join)
    X = df1['Preprocessed_Text2']
    y = df1['Category']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    tf_vec = TfidfVectorizer()
    train_features = tf_vec.fit(X_train)
    train_features = tf_vec.transform(X_train)
    test_features = tf_vec.transform(X_test)

    nb = MultinomialNB()

    results = fit_eval_model(nb, train_features, y_train, test_features, y_test)

    print(articles[2]['title'] + "is in category:" + classify_article(tf_vec, nb, articles[2]['content']))

    to_summarize = ""

    for i in similar_article_indices:
        to_summarize += run_GPT4(index_to_article[i])

    print(run_GPT4(to_summarize))


# You can now analyze the content of the articles
# The 'articles' variable is a list of dictionaries containing the headline, link, publication_date, and content of each article

