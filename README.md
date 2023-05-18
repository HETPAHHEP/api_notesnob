# API NoteSnob

## Создание секретного ключа JWT

```bash
openssl rand -hex 32
```

## Создание секретного ключа Django

```bash
./manage.py shell -c "from django.core.management import utils; 
print('django-insecure-' + utils.get_random_secret_key())"
```