from django.apps import AppConfig


class LogcheckerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.logchecker'

    def ready(self):
        print("Starting APScheduler...")
        from .jobs import scheduler
        # scheduler.start()

