# Generated by Django 4.2.1 on 2023-05-08 19:41

from django.db import migrations, models

import api.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=150, validators=[api.validators.UsernameValidator()])),
                ('confirmation_code', models.CharField(max_length=6)),
                ('expires_at', models.DateTimeField()),
            ],
        ),
    ]
