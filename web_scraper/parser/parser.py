import json
import time

import requests
from bs4 import BeautifulSoup as bs


def get_main_page():
    url = 'https://habr.com/ru/'
    response = requests.get(url)
    return response.text


def parse_main_page(html):
    soup = bs(html, 'html.parser')
    hub_links = soup.find_all('a', class_="tm-title__link")
    article_links = ["https://habr.com"+link['href'] for link in hub_links]
    return article_links


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
    author_url = 'https://habr.com'+author_content['href']

    return {
        'title': title,
        'date': date,
        'article_url': article_url,
        'author_name': author_name,
        'author_url': author_url
    }


def print_article_info(info):
    print("\nArticle Information:")
    print(f"Title: {info['title']}")
    print(f"Date: {info['date']}")
    print(f"URL: {info['article_url']}")
    print(f"Author: {info['author_name']}")
    print(f"Author URL: {info['author_url']}")
    print("-" * 50)


def main():
    while True:
        print("Получаю данные с Хабра...")
        main_page_html = get_main_page()
        article_links = parse_main_page(main_page_html)
        articles = []

        for article_link in article_links:
            info = parse_article_page(article_link)
            # print_article_info(info)
            articles_info = dict()
            articles_info['title'] = info['title']
            articles_info['date'] = info['date']
            articles_info['article_url'] = info['article_url']
            articles_info['author_name'] = info['author_name']
            articles_info['author_url'] = info['author_url']
            articles.append(articles_info)

        print("Жду 10 минут...")
        time.sleep(600)  # Wait for 10 minutes


if __name__ == '__main__':
    main()
