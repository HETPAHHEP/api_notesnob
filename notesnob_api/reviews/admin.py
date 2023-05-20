from django.contrib import admin

from .models import Genre, Comment, Category, Review, Title


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'category']
    list_filter = ['year', 'category']
    search_fields = ['name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'author', 'score', 'pub_date']
    list_filter = ['score', 'pub_date']
    search_fields = ['title__name', 'text', 'author__username']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['review', 'text', 'author', 'pub_date']
    list_filter = ['pub_date']
    search_fields = ['text', 'review__text', 'author__username']
