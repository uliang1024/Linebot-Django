from pathlib import Path
from mongoengine import connect

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-z9fth!vpz4p2j5%d3asj)%r+i8ako&b@qfp)98ycie+l=mtomo'

DEBUG = True

ALLOWED_HOSTS = ['tasktrackbot-amisleo000.b4a.run']
# ALLOWED_HOSTS = ['127.0.0.1']

connect("linebot", host="mongodb+srv://amisleo000:AMISleo123@cluster0.3dwwur1.mongodb.net")

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

import requests

def my_task():
    requests.post("https://notify-api.line.me/api/notify", 
                  headers = {"Authorization": "Bearer " + '3t3o0JGWlcQfcv21kc4IBdM6uyyPlVhBSgxQOZTFNUM', 
                             "Content-Type" : "application/x-www-form-urlencoded"}, 
                  params = {'message': '別再混了 !'})
    
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

# 注册定时任务，每分钟执行一次
scheduler.add_job(my_task, "interval", minutes=1)

# 启动任务调度器
scheduler.start()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django_apscheduler',
    'leetcodelinebot.apps.LeetcodelinebotConfig',
    'rest_framework',
    'rest_framework_mongoengine',
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
        'ENGINE': '',
    }
}

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