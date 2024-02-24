import os
from django.core.wsgi import get_wsgi_application

# Substitua 'myproject.settings' pelo caminho correto para seus arquivos de configuração
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'merkadu.settings_prod'))

application = get_wsgi_application()
