from django.apps import AppConfig


class AdvertiserConfig(AppConfig):
    name = 'advertiser'

    def ready(self):
        from rag.rag_service import index_all_spaces
        index_all_spaces()