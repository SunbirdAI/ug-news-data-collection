import re
import requests
from bs4 import BeautifulSoup
from news.news import News


class Observer(News):
    def __init__(self):
        url = "https://www.observer.ug"
        super().__init__(url)

    def fetch_news(self):
        """Fetch data from the Observer online newspaper"""

        # Go to the headlines page
        news_request = requests.get(self.url + "/news/headlines")
        headlines_page = news_request.content
        soup1 = BeautifulSoup(headlines_page, 'html5lib')

        div = soup1.find('div', class_='nspMain')
        article_links = div.find_all('a')
        print(article_links)
        print(len(article_links))