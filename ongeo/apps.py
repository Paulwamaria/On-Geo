from __future__ import unicode_literals
from django.apps import AppConfig


class OngeoConfig(AppConfig):
    name = 'ongeo'


    def ready(self):
        import ongeo.signals