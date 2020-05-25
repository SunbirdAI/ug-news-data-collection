import requests
from bs4 import BeautifulSoup
from news.news import News


class NewVision(News):

    def __init__(self):
        url = "https://www.newvision.co.ug"
        article_href = "https://www.newvision.co.ug/new_vision/news/"
        super().__init__(url, article_href)

    def clean_article_text(self, paragraphs):
        del paragraphs[0:2]
        del paragraphs[-7:]
        cleaned_text = []
        for p in paragraphs:
            p_text = p.get_text().strip()
            cleaned_text.append(p_text)
        return " ".join(cleaned_text)

    def fetch_news(self):
        """Fetch data from the New Vision online newspaper"""

        # Go to the local news page
        news_request = requests.get(self.url + "/local")
        coverpage = news_request.content
        soup1 = BeautifulSoup(coverpage, 'html5lib')

        # Pick out the divs that hold links to news articles
        divs1 = soup1.find_all('div')
        divs2 = divs1[2].find_all('div', id='wrapper-container')
        article_links = divs2[0].find_all('a')

        # Follow each link and fetch the article content
        all_articles = []

        for link in article_links:
            if "/news" in link['href']:
                article = requests.get(self.url + link['href'])
                article_content = article.content
                soup2 = BeautifulSoup(article_content, 'html5lib')
                title = soup2.find('h1').get_text()
                slug = "-".join(title.split())
                paragraphs = soup2.find_all('p', recursive=True)
                cleaned_article = self.clean_article_text(paragraphs)
                all_articles.append({'slug': slug, 'text': cleaned_article})

        return all_articles
