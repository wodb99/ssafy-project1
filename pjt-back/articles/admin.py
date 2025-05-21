from django.contrib import admin
from .models import Article, Comment  # models.py에서 가져오기

admin.site.register(Article)
admin.site.register(Comment)