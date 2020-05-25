import re
import requests
from bs4 import BeautifulSoup
from news.news import News

class NewVision(News):

    def __init__(self):
        self.url = "https://www.newvision.co.ug/local"
        self.article_href = re.compile(r"https://www.newvision.co.ug/new_vision/news/")


    def clean_article_text(self, paragraphs):
        del paragraphs[0:2]
        del paragraphs[-7:]
        cleaned_text = []
        for p in paragraphs:
            p_text = p.get_text().strip()
            cleaned_text.append(p_text)
        return " ".join(cleaned_text)
        
    def fetch_news(self, url):
        """Fetch data from the New Vision online newspaper"""

        news_request = requests.get(self.url)
        coverpage = news_request.content
        
        # Pick out the anchor tags to get the links to the actual news articles
        soup1 = BeautifulSoup(coverpage, 'html5lib')
        article_links = soup1.find_all(href=self.article_href)
                
        # Follow each link and fetch the article content
        all_articles = []

        for link in article_links:
            article = requests.get(link['href'])
            article_content = article.content
            soup2 = BeautifulSoup(article_content, 'html5lib')
            title = soup2.find('h1').get_text()
            slug = "-".join(title.split())
            paragraphs = soup2.find_all('p', recursive=True)
            cleaned_article = self.clean_article_text(paragraphs)
            all_articles.append({'slug': slug, 'text': cleaned_article})
                
        return all_articles
