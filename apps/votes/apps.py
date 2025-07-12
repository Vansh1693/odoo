from django.apps import AppConfig


class VotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.votes'

    def ready(self):
        import apps.votes.signals
