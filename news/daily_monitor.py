import re
import requests
from bs4 import BeautifulSoup
from news.news import News


class DailyMonitor(News):
    def __init__(self):
        url = "https://www.monitor.co.ug"
        article_href = re.compile(url)
        super().__init__(url, article_href)

    def clean_article_text(self, paragraphs):
        # del paragraphs[0:2]
        # del paragraphs[-7:]
        cleaned_text = []
        for p in paragraphs:
            p_text = p.get_text().strip()
            cleaned_text.append(p_text)
        return " ".join(cleaned_text)

    def fetch_news(self):
        """Fetch data from the Daily Monitor online newspaper"""

        # Find the link to the national news page
        news_request = requests.get(self.url)
        coverpage = news_request.content
        soup1 = BeautifulSoup(coverpage, 'html5lib')
        national_news_page = soup1.nav.find_all('a')[1]

        # Follow the national news link and pick out
        # links to individual articles
        national_news = requests.get(self.url + national_news_page['href'])
        national_news_content = national_news.content
        soup2 = BeautifulSoup(national_news_content, 'html5lib')
        article_links = soup2.find_all('a')

        # Follow each link and fetch the article content

        all_articles = []

        for link in article_links:
            article = requests.get(self.url + link['href'])
            article_content = article.content
            soup2 = BeautifulSoup(article_content, 'html5lib')
            title = soup2.find('h1').get_text()
            slug = "-".join(title.split())
            paragraphs = soup2.find_all('p', recursive=True)
            cleaned_article = self.clean_article_text(paragraphs)
            all_articles.append({'slug': slug, 'text': cleaned_article})

        return all_articles
