from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'date', 'article_url', 'author_name', 'author_url')
    search_fields = ('title', 'author_name',)
    list_filter = ('date', )
    empty_value_display = '-нет_данных-'


admin.site.register(Article, ArticleAdmin)
