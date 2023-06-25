from pathlib import Path
from mongoengine import connect

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-z9fth!vpz4p2j5%d3asj)%r+i8ako&b@qfp)98ycie+l=mtomo'

DEBUG = True

ALLOWED_HOSTS = ['tasktrackbot-amisleo000.b4a.run']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'leetcodelinebot.apps.LeetcodelinebotConfig',
    'django_mongoengine',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tasktrackbot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tasktrackbot.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

connect(host="mongodb://admin:CRW5IYF6L2akAaFvqag6oouz@MongoS3601A.back4app.com:27017/d7b31b754ebb4b1982d18d2a08d932dd")

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LINE_CHANNEL_ACCESS_TOKEN = 'ynggtFXVAyqtYCOMT+WI4bNQoCXeHd6TOgEERvI7gQCwB4ZqtKJ/UF/xLN3IwszdePcgiozRuCAN52GYa80V0/qFCLvDciH0LNzmNXiwNexDvtFJHoo/Oy9Ao5ImY/podCy+B41/cyjXVvh5YCkvuwdB04t89/1O/w1cDnyilFU='
 
LINE_CHANNEL_SECRET = '47148d9659ff48b3e87af59acdebbb3e'