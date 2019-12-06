# Allofood

### A food ordering website built with Django

<br><br>

#### Requirements:
- python 3
- django 2

#### Usage:


allofood> ```python manage.py runserver```


#### Things you need to include on your `settings.py` file:
- 'allofood.apps.AllofoodConfig' and 'crispy_forms' among your `INSTALLED_APPS`
- CRISPY_TEMPLATE_PACK = 'bootstrap4'

- EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
- EMAIL_HOST = 'smtp.gmail.com'
- EMAIL_HOST_USER  = 'your gmail address'
- EMAIL_HOST_PASSWORD = 'your gmail password'
- EMAIL_PORT = 587
- EMAIL_USE_TLS = True




