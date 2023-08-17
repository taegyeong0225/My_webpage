from django.contrib import admin # 관리자 페이지
from .models import Post, Category, Tag, Comment # models.py에서 import
from markdownx.admin import MarkdownxModelAdmin

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

# Django 관리자 사이트에서 모델을 등록하는 역할
admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)