from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'date', 'article_url', 'author_name', 'author_url', 'text')
    search_fields = ('pk', 'title', 'author_name', 'text')
    list_filter = ('date', 'author_name', )
    empty_value_display = '-нет_данных-'


admin.site.register(Article, ArticleAdmin)
