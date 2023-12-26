from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    article_url = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    author_url = models.CharField(max_length=200)
