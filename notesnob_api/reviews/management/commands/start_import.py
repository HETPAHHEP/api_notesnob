import os
from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import CustomUser

from notesnob_api.settings import BASE_DIR


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from CSV files for NoteSnob API database"

    @staticmethod
    def title_case(model, row):
        title = model.objects.create(
            id=row['id'], name=row['name'], year=row['year'])

        category_id = row['category']
        category = Category.objects.filter(id=category_id).first()
        if category:
            title.category = category
            title.save()

    @staticmethod
    def genre_title_case(model, row):
        genre_id = row['genre_id']
        genre = Genre.objects.filter(id=genre_id).first()

        title_id = row['title_id']
        title = Title.objects.filter(id=title_id).first()

        if genre and title:
            model.objects.create(id=row['id'], genre=genre, title=title)

    @staticmethod
    def review_case(model, row):
        title_id = row['title_id']
        title = Title.objects.filter(id=title_id).first()

        author_id = row['author']
        author = CustomUser.objects.filter(id=author_id).first()

        if title and author:
            model.objects.create(
                id=row['id'],
                title=title,
                text=row['text'],
                author=author,
                score=row['score'],
                pub_date=row['pub_date']
            )

    @staticmethod
    def comment_case(model, row):
        review_id = row['review_id']
        review = Review.objects.filter(id=review_id).first()

        author_id = row['author']
        author = CustomUser.objects.filter(id=author_id).first()

        if review and author:
            model.objects.create(
                id=row['id'],
                review=review,
                text=row['text'],
                author=author,
                pub_date=row['pub_date']
            )

    def handle(self, *args, **options):
        csv_file_names = {
            'users.csv': CustomUser,
            'category.csv': Category,
            'genre.csv': Genre,
            'titles.csv': Title,
            'genre_title.csv': GenreTitle,
            'review.csv': Review,
            'comments.csv': Comment,
        }

        for csv_file, model in csv_file_names.items():
            path_to_csv = os.path.join(BASE_DIR, 'static/data/', csv_file)

            with open(path_to_csv, 'r', encoding='utf-8') as file:
                reader = DictReader(file)
                warning_status = False

                for row in reader:

                    try:
                        model.objects.create(**row)
                    except ValueError:
                        warning_status = True

                        if model.__name__ == Title.__name__:
                            self.title_case(model, row)

                        elif model.__name__ == GenreTitle.__name__:
                            self.genre_title_case(model, row)

                        elif model.__name__ == Review.__name__:
                            self.review_case(model, row)

                        elif model.__name__ == Comment.__name__:
                            self.comment_case(model, row)

            if warning_status:
                self.stdout.write(self.style.WARNING(
                    f'Import case for {model.__name__} data in {csv_file}'))

            self.stdout.write(self.style.SUCCESS(
                f'{model.__name__} data from {csv_file} imported successfully'))
