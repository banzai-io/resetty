from django.apps import AppConfig

class ResettyAppConfig(AppConfig):
    name = 'resetty'

    def ready(self):
        import resetty.signals
