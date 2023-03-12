from datetime import datetime

import requests
from bs4 import BeautifulSoup

from webapp.model import db
from webapp.news.model import News


def get_html(url):
    try:
        result = requests.get(url, timeout=5)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def get_python_news():
    html = get_html("https://www.python.org/blogs/")

    if html:
        soup = BeautifulSoup(html, "html.parser")
        news_list = soup.find("ul", class_="list-recent-posts").find_all("li")
        for news in news_list:
            title = news.find("a").text
            url = news.find("a")["href"]
            published = news.find("time")["datetime"]
            print(published)
            try:
                published = datetime.strptime(published, "%Y-%m-%d")
            except ValueError:
                published = datetime.now()
            save_news(title=title, url=url, published=published)


def save_news(title, url, published):
    news_exist = News.query.filter(News.url == url).count()

    if not news_exist:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()


if __name__ == "__main__":
    get_python_news()
