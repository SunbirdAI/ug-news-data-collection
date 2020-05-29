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

        div = soup1.find('div', id='nsp-newslist')
        article_links = [a['href'] for a in div.find_all('a')]
        article_links = list(set(article_links))

        # Follow each link and fetch the article content
        all_articles = []

        for link in article_links:
            link = self.url + link
            article = requests.get(link)
            article_content = article.content
            soup2 = BeautifulSoup(article_content, 'html5lib')
            soup3 = soup2.find('article', class_='item-page')
            if soup3:
                title = soup3.find('h1').get_text()
                print(title)
                slug = "-".join(title.split())
                paragraphs = soup3.find_all('p', recursive=True)
                cleaned_article = self.clean_article_text(paragraphs)
                all_articles.append({'slug': slug, 'text': cleaned_article})

        return all_articles
