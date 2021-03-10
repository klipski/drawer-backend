from django.apps import AppConfig


class DrawerConfig(AppConfig):
    name = 'drawer'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from drawer import signals
