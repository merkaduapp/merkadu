from pathlib import Path
import os
# from decouple import config
from flask import Flask
from flask_mail import Mail, Message
import mimetypes
import dj_database_url
import secrets
import django_on_heroku
from decouple import config

# if os.environ.get('HEROKU', None):
#     from .heroku_settings import *
# else:
#     from .settings import *

SECRET_KEY = secrets.token_hex(32)


app = Flask(__name__)
mail= Mail(app)

DEBUG = config('DEBUG', cast=bool, default=False)
DJANGO_SETTINGS_MODULE = config('DJANGO_SETTINGS_MODUL', default='merkadu.settings')
ALLOWED_HOSTS = ['3.22.61.108', 'www.merkaduapp.com', ".railway.app"]



mimetypes.add_type("image/webp", ".webp", True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuração de logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'debug.log'),
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file', 'console'],  # Adicionando o console para exibir no terminal
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
# BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



SECRET_KEY = 'django-insecure-zn0j_kavg5i@7(80etsz4g8wry-4r9g)h!#-4l(&a$&g(ep0-d'

DEBUG = True

# ALLOWED_HOSTS = ['localhost', '127.0.0.1',]
ALLOWED_HOST = ['*']


MERCADO_PAGO_ACCESS_TOKEN = "APP_USR-1981258799368909-120418-44705d4fa27c6aa40d60636252959bd1-738308629"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.auth',
    'cloudinary_storage',
    'cloudinary',
    'anymail',
    'merkadu',
    'widget_tweaks',
    "sslserver",
    "app",
    'rest_framework',
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    # Outras configurações do Django REST Framework, se necessário...
}

SITE_ID = 1

AUTH_USER_MODEL = 'app.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

THUMBNAIL_PROCESSORS = [
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # Adicione outros backends de autenticação, se necessário
]

FILER_IS_PUBLIC_DEFAULT = True

ROOT_URLCONF = 'merkadu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'merkadu.wsgi.application'

LOGIN_URL = 'login'  # Use o nome da URL personalizada que você definiu

AUTH_USER_MODEL = 'app.CustomUser'


HEROKU_DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR + 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', default='db.sqlite3'),
        'USER': os.getenv('DB_USER', default=''),
        'PASSWORD': os.getenv('DB_PASSWORD', default=''),
        'HOST': os.getenv('DB_HOST', default=''),
        'PORT': os.getenv('DB_PORT', default=''),
    }
}

if 'DYNO' in os.environ:  # Verifica se está no ambiente do Heroku
    DATABASES = HEROKU_DATABASES

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': '722435',
#         'HOST': 'database-1.cn4k24kk8v5u.us-east-2.rds.amazonaws.com',
#         'PORT': '5432',  
#     }
# }


# DATABASES = {
#     'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
# }

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/Users/mac/projects/merkadu/merkadu/wsgi.py',  # Especifique o caminho do arquivo de log
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_I18N = True

USE_L10N = True

USE_TZ = True


SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7


# EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
# DEFAULT_FROM_EMAIL = 'no-reply@merkadu.shop'
# SERVER_EMAIL = DEFAULT_FROM_EMAIL
# ANYMAIL = {
#     "MAILGUN_API_KEY": config('MAILGUN_API_KEY', default=''),
#     "MAILGUN_SENDER_DOMAIN": config('MAILGUN_SENDER_DOMAIN', default=''),
# }
# STATIC_ROOT = '/static/'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'merkaduapp@gmail.com'
# EMAIL_HOST_PASSWORD = 'Ra313105514$'

CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
CLOUDFLARE_API_KEY = os.getenv('CLOUDFLARE_API_KEY')
CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'merkaduapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ra313105514$'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['DEFAULT_FROM_EMAIL'] = 'no-reply@merkadu.app'
mail = Mail(app)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# # settings.py

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Alterado para um diretório diferente de STATICFILES_DIRS

STATICFILES_IGNORE_PATTERNS = ['*.js']

django_on_heroku.settings(locals())
