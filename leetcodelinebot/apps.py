from django.apps import AppConfig


class LeetcodelinebotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leetcodelinebot'

    def ready(self):
        import django_mongoengine
        django_mongoengine.monkey_patch()