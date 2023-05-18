from django.db import models

from users.models import CustomUser

from .validators import ActualYearValidator, SlugValidator

# Выбор оценки произведения от 1 до 10
SCORE_CHOICES = [(i, i) for i in range(1, 11)]


class Category(models.Model):
    """Модель категорий произведения (Фильм, Музыка, Книга и тд)"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)
    # slug = models.SlugField(max_length=50, unique=True, validators=[SlugValidator()])


class Genre(models.Model):
    """Модель жанра произведения"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Title(models.Model):
    """Модель произведения"""
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[ActualYearValidator()])
    description = models.CharField(blank=True)
    gener = models.ManyToManyField(Genre, on_delete=models.SET_NULL, through='genre_title')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='titles')


class Review(models.Model):
    """Модель обзора на произведение"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Модель комментария к обзору"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
