from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect


class CmdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cmdb'
    
    def ready(self):
        print('~~cmdb项目加载，建立MongoDB连接~~')
        connect(**settings.MONGODB_DATABASES)
