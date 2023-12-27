import asyncio
import json
import logging
import time
import sys

import aiohttp
from bs4 import BeautifulSoup as bs
from django.core.management.base import BaseCommand

from ...models import Article


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Command(BaseCommand):
    help = "Передача данных в базу данных"
    articles = []

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get_main_page(self):
        url = "https://habr.com/ru/"
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, url)
        return html

    async def parse_main_page(self, html):
        soup = bs(html, "html.parser")
        hub_links = soup.find_all("a", class_="tm-title__link")
        article_links = ["https://habr.com" + link["href"] for link in hub_links]
        return article_links

    async def parse_article_page(self, session, article_url):
        async with session.get(article_url) as response:
            if response.status != 200:
                logger.error(response.status)
                return None

            soup = bs(await response.text(), "html.parser")

            script_content = soup.find(
                "script", {"data-vue-meta": "ssr", "type": "application/ld+json"}
            ).string
            author_content = soup.find("a", class_="tm-user-info__username")
            data = json.loads(script_content)
            title = data.get("headline", "")
            date = data.get("datePublished", "")
            author_name = data.get("author", "").get("name")
            if author_content:
                author_url = "https://habr.com" + author_content.get("href")
            else:
                author_url = "empty"

            post = soup.find(
                "div",
                class_="article-formatted-body article-formatted-body article-formatted-body_version-2",
            )
            if post:
                text = post.text
            else:
                text = "empty"

            return {
                "title": title,
                "date": date,
                "article_url": article_url,
                "author_name": author_name,
                "author_url": author_url,
                "text": text,
            }

    async def parse_articles(self, article_links):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.parse_article_page(session, article_link)
                for article_link in article_links
            ]
            return await asyncio.gather(*tasks)

    async def async_parse(self):
        main_page_html = await self.get_main_page()
        article_links = await self.parse_main_page(main_page_html)
        self.articles = await self.parse_articles(article_links)

    def handle(self, *args, **options):
        while True:
            logger.info("Получение данных с Хабра")
            asyncio.run(self.async_parse())
            logger.info("Перенос обновлений в БД")

            for article_data in self.articles:
                if article_data:
                    existing_article = Article.objects.filter(
                        article_url=article_data["article_url"]
                    ).first()

                    if not existing_article:
                        Article.objects.create(
                            title=article_data["title"],
                            date=article_data["date"],
                            article_url=article_data["article_url"],
                            author_name=article_data["author_name"],
                            author_url=article_data["author_url"],
                            text=article_data["text"],
                        )

            logger.info("Ожидание 10 минут")
            time.sleep(600)
