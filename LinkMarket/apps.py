from django.apps import AppConfig


class LinkMarketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LinkMarket'
    
    def ready(self):
        import LinkMarket.signals
