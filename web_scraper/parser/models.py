from django.db import models

from .parser import articles


class Article(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField(max_length=200)
    article_url = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    author_url = models.CharField(max_length=200)
