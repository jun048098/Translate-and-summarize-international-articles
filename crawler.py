from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import json
import time

def extract_links(url: str, html_class: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    a_s = soup.find_all("a", class_=html_class)
    links = [links['href'] for links in a_s]
    full_links = [url + link for link in links]

    return full_links


def extract_articles(links_list: list, title_class: str, paragraph_class: str):
    articles = []
    for link in links_list:
        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.text, "html.parser")

        article_title = article_soup.find("h1", class_=title_class)
        
        article_texts = article_soup.find_all("p", class_=paragraph_class)
        real_article_texts = [text.get_text(strip=True).replace("\xa0", " ") for text in article_texts]
        article = f"# {article_title.get_text(strip=True)}"
        for idx, text in enumerate(real_article_texts):
            article += f"\n{text}"
    
        articles.append(article)
    time.sleep(1)
    return articles