import os
from django.conf import settings

def configure_django_settings():
    # Define o DJANGO_SETTINGS_MODULE
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'merkadu.settings')

    # Configura as configurações do Django
    settings.configure()
