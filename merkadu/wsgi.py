import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define o módulo de configurações do Django com base na variável de ambiente
# Se 'DJANGO_SETTINGS_MODULE' não estiver definida, utiliza 'merkadu.settings_prod' como padrão
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'merkadu.settings_prod'))

application = get_wsgi_application()
