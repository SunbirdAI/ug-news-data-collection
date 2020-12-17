import unittest
from bs4 import BeautifulSoup
from news import (
    NewVision, DailyMonitor, Observer
)


class TestNews(unittest.TestCase):
    def setUp(self):
        self.new_vision = NewVision()
        self.daily_monitor = DailyMonitor()
        self.observer = Observer()
        html = "<p> \t\t First paragraph</p> <p>Second paragraph</p> \n\n "
        soup = BeautifulSoup(html, 'html5lib')
        self.paragraphs = soup.find_all('p')

    def test_clean_empty_article(self):
        cleaned = self.new_vision.clean_article_text([])
        self.assertEqual(cleaned, "")

    def test_clean_article_with_white_space(self):
        cleaned = self.new_vision.clean_article_text(self.paragraphs)
        self.assertEqual(cleaned, "First paragraph Second paragraph")

    def test_fetch_news(self):
        pass
