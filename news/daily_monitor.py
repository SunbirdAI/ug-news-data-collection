import requests
from bs4 import BeautifulSoup
from .news import News


class DailyMonitor(News):
    def __init__(self):
        url = "https://www.monitor.co.ug"
        super().__init__(url)

    def fetch_news(self):
        """Fetch data from the Daily Monitor online newspaper"""

        # Find the link to the national news page
        news_request = requests.get(self.url)
        coverpage = news_request.content
        soup1 = BeautifulSoup(coverpage, 'html5lib')
        links_div = soup1.nav.find('div', class_='col-3')
        national_news_href = '/uganda/news/national'
        national_news_page = links_div.find_all(
            'a', href=national_news_href
        )

        # Follow the national news link and pick out
        # links to individual articles
        national_news = requests.get(self.url + national_news_page[0]['href'])
        national_news_content = national_news.content
        soup2 = BeautifulSoup(national_news_content, 'html5lib')
        column = soup2.find('div', class_='main column')
        article_links = [a['href'] for a in column.find_all('a')]
        article_links = list(set(article_links))
        article_links.remove(national_news_href)

        # Follow each link and fetch the article content
        all_articles = []

        for link in article_links:
            if self.url not in link:
                link = self.url + link
            article = requests.get(link)
            soup2 = BeautifulSoup(article.content, 'html5lib')
            title = soup2.find('h2')
            if title:
                title = title.get_text()
            slug = "-".join(title.split())
            paragraphs = soup2.find_all('p', recursive=True)
            cleaned_article = self.clean_article_text(paragraphs)
            all_articles.append({'slug': slug, 'text': cleaned_article})

        return all_articles
