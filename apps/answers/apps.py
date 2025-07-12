from django.apps import AppConfig


class AnswersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.answers'

    def ready(self):
        import apps.answers.signals
