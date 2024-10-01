from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import time
import re
from datetime import datetime
import yaml

with open("crawl_class.yaml") as f:
    classes = yaml.load(f, Loader=yaml.FullLoader)

def extract_links(url: str, html_class: str):
    """
    prototype code
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    a_s = soup.find_all("a", class_=html_class)
    links = [links['href'] for links in a_s]
    full_links = set(url + link for link in links)

    return list(full_links)

def extract_cnn_links_re(url: str, html_class_regex: re.Pattern):
    """
    1. CNN에서 `container__link container__link`로 시작하는 class의 링크만 가져온다.
    2. `/연도/월/일/` 패턴으로 시작하는 링크만 가져온다.
    3. 오늘의 기사만 가져온다.

    Args:
        url: cnn의 기본 url
        html_class_regex: html class의 공통 패턴 정규식
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    a_s = soup.find_all("a", class_=html_class_regex)

    today = datetime.today()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    day = today.strftime('%d')
    date_pattern = re.compile(f"^/{year}/{month}/{day}/")

    links = []
    for a_tag in a_s:
        href = a_tag.get("href", "")
        if date_pattern.match(href):
            links.append(href)
    
    full_links = set(url + link for link in links)

    return list(full_links)

def extract_cnn_articles(links_list: list, title_class_regex: re.Pattern, paragraph_class_regex: re.Pattern):
    """
    cnn에서 가져온 기사에서 제목과 문단 글을 가져온다.

    Args:
        links_list: `extract_cnn_links_re`함수에서 return된 기사 link로 구성된 list
        title_class_regex: 기사 제목 class의 공통 패턴 정규식
        paragraph_class_regex: 기사 문단 class의 공통 패턴 정규식
    """
    articles = []
    for link in links_list:
        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.text, "html.parser")

        article_title = article_soup.find("h1", class_=title_class_regex)
        
        article_texts = article_soup.find_all("p", class_=paragraph_class_regex)
        real_article_texts = [text.get_text(strip=True).replace("\xa0", " ") for text in article_texts]
        article = f"# {article_title.get_text(strip=True)}"
        for idx, text in enumerate(real_article_texts):
            article += f"\n{text}"
    
        articles.append(article)
        time.sleep(1)
    return articles

def extract_aljazeera_articles(links_list: list, title_class: str, paragraph_class: str):
    """
    Aljazeera에서 <link>태그 중 `data-chunk`값이 `article-route`인 기사를 가져온다.
    """
    articles = []
    article_route = False
    liveblog_route = False
    for link in links_list:
        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.text, "html.parser")
        html_values = article_soup.find_all('link', attrs = {'data-chunk': True})

        for v in html_values:
            if v.get("data-chunk") == "article-route":
                print("article-route")
                article_route = True
                break
            elif v.get("data-chunk") == "liveblog-route":
                print("liveblog-route")
                liveblog_route = True
                break
            else:
                print("False")
                return "Error"

        if article_route == True:
            header_values = article_soup.find_all('header', class_=title_class)
            title = header_values[0].find_all("h1")[0].get_text(strip=True)
            article = f"# {title}"
            
            p_values = article_soup.find_all('div', class_=paragraph_class)
            for value in p_values:
                texts = value.find_all('p')
                for p in texts:
                    text = p.get_text()
                    article += f"\n{text}"
                articles.append(article)
            article_route = False

        time.sleep(1)
    return articles


def crawling():
    """
    cnn daily 기사의 링크들과 본문들을 긁어온다.
    """
    daily_ptn = re.compile(fr"{classes['CNN_DAILY_ARTICLE_PTN']}")
    link_list = extract_cnn_links_re(classes['CNN_URL'], daily_ptn)

    title_ptn = re.compile(r"^headline__text")
    paragraph_ptn = re.compile(r"^paragraph")
    text_list = extract_cnn_articles(link_list, title_ptn, paragraph_ptn)

    return text_list, link_list

