import json
import time
import requests
from bs4 import BeautifulSoup as bs
from django.core.management.base import BaseCommand

from ...models import Article


class Command(BaseCommand):
    help = 'Transserfing data to database'
    articles = []

    @staticmethod
    def get_main_page():
        url = 'https://habr.com/ru/'
        response = requests.get(url)
        return response.text

    @staticmethod
    def parse_main_page(html):
        soup = bs(html, 'html.parser')
        hub_links = soup.find_all('a', class_="tm-title__link")
        article_links = ["https://habr.com" + link['href'] for link in hub_links]
        return article_links

    @staticmethod
    def parse_article_page(article_url):
        response = requests.get(article_url)
        if response.status_code != 200:
            print(response.status_code)
        soup = bs(response.text, 'html.parser')

        script_content = soup.find('script', {'data-vue-meta': 'ssr', 'type': 'application/ld+json'}).string
        author_content = soup.find('a', class_='tm-user-info__username')
        data = json.loads(script_content)
        title = data.get('headline', '')
        date = data.get('datePublished', '')
        author_name = data.get('author', '').get('name')
        if author_content:
            author_url = 'https://habr.com' + author_content.get('href')
        else:
            author_url = 'empty'
        post = soup.find('div', class_='article-formatted-body article-formatted-body article-formatted-body_version-2')
        if post:
            text = post.text
        else:
            text = 'empty'

        return {
            'title': title,
            'date': date,
            'article_url': article_url,
            'author_name': author_name,
            'author_url': author_url,
            'text': text
        }

    @staticmethod
    def print_article_info(info):
        print("\nArticle Information:")
        print(f"Title: {info['title']}")
        print(f"Date: {info['date']}")
        print(f"URL: {info['article_url']}")
        print(f"Author: {info['author_name']}")
        print(f"Author URL: {info['author_url']}")
        print("-" * 50)

    def parse(self):
        main_page_html = Command.get_main_page()
        article_links = Command.parse_main_page(main_page_html)
        for article_link in article_links:
            info = Command.parse_article_page(article_link)
            articles_info = dict()
            articles_info['title'] = info['title']
            articles_info['date'] = info['date']
            articles_info['article_url'] = info['article_url']
            articles_info['author_name'] = info['author_name']
            articles_info['author_url'] = info['author_url']
            articles_info['text'] = info['text']
            self.articles.append(articles_info)

    def handle(self, *args, **options):
        while True:
            print("Получаю данные с Хабра...")
            self.parse()
            print('Обновляю данные в БД')

            for article_data in self.articles:
                if article_data:
                    existing_article = Article.objects.filter(article_url=article_data['article_url']).first()

                    if not existing_article:
                        Article.objects.create(
                            title=article_data['title'],
                            date=article_data['date'],
                            article_url=article_data['article_url'],
                            author_name=article_data['author_name'],
                            author_url=article_data['author_url'],
                            text=article_data['text']
                        )

            print("Жду 10 минут...")
            time.sleep(600)
