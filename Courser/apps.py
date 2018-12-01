from django.apps import AppConfig


class CourserConfig(AppConfig):
    name = 'Courser'

    def ready(self):
        from . import signals
