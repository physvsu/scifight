# SECURITY WARNING: keep the secret key used in production secret!
# You can generate secret key on this site:
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = 'your_secret_key'


# database options
# MySQL DB
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'scifight',
        'USER':     'user',
        'PASSWORD': 'password',
        'HOST':     'localhost',
        'PORT':     3306
    }
}

DEBUG = True

ALLOWED_HOSTS = []