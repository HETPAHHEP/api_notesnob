from django.db import models

from users.models import CustomUser

from .validators import validate_year

# Выбор оценки произведения от 1 до 10
SCORE_CHOICES = [(i, i) for i in range(1, 11)]


class Category(models.Model):
    """Модель категорий произведения (Фильм, Музыка, Книга и тд)"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения"""
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[validate_year])
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='titles')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Сводная таблица отношения ManyToMany для произведения и жанров"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Модель обзора на произведение"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'], name='unique_title_author_match')
        ]

    def __str__(self):
        return self.text[:40]


class Comment(models.Model):
    """Модель комментария к обзору"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:40]
