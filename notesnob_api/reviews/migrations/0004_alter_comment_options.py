# Generated by Django 4.2.1 on 2023-05-19 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_rename_gener_title_genre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-pub_date']},
        ),
    ]
