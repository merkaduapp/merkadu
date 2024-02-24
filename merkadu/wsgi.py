import os

from django.core.wsgi import get_wsgi_application

# Define o ambiente atual com base em uma variável de ambiente
# Por exemplo, você pode definir a variável de ambiente 'ENVIRONMENT'
# para 'local', 'development' ou 'production'.
environment = os.getenv('ENVIRONMENT', 'local')

# Determina qual arquivo de configuração do Django será usado com base no ambiente
if environment == 'local':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'merkadu.settings_local')
elif environment == 'development':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'merkadu.settings_dev')
elif environment == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'merkadu.settings_prod')

# Obtém a aplicação WSGI do Django
application = get_wsgi_application()