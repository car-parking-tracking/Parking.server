import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Custom user model:
AUTH_USER_MODEL = 'users.CustomUser'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'backend',
    str(os.getenv('HOST_ADDRESS')),
    str(os.getenv('HOST_ADDRESS')),
    'parkonaft.acceleratorpracticum.ru',
    'https://parkonaft.acceleratorpracticum.ru'
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'http://127.0.0.1',
    'http://' + str(os.getenv('HOST_ADDRESS')),
    'https://' + str(os.getenv('HOST_ADDRESS')),
    'http://parkonaft.acceleratorpracticum.ru',
    'https://parkonaft.acceleratorpracticum.ru',
]

BASE_URL = os.getenv('BASE_URL', default='/api/v1/users/')

# DJOSER SETTINGS
DJOSER = {
    "LOGIN FIELD": "email",
    "SEND_ACTIVATION_EMAIL": False,  # убрать после релиза
    "SEND_CONFIRMATION_EMAIL": False,  # убрать после релиза
    # "PASSWORD_RESET_CONFIRM_URL": f"{BASE_URL}reset_password/{{uid}}/{{token}}/",
    "ACTIVATION_URL": f"{BASE_URL}activation/{{uid}}/{{token}}/",
    'SERIALIZERS': {
        # 'token_create': 'api.serializers.CustomTokenCreateSerializer',
        'token': 'djoser.serializers.TokenSerializer',
        'token_create': 'djoser.serializers.TokenCreateSerializer',
        'user': 'api.serializers.CustomUserSerializer',
        'current_user': 'api.serializers.CustomUserSerializer',
        'create_user': 'api.serializers.CustomUserCreateSerializer',
        'activation': 'djoser.serializers.ActivationSerializer',
    },
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'parking_lots.apps.ParkingLotsConfig',
    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
    'django_filters',
    'drf_yasg',
    'core.apps.CoreConfig',
    'users',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

ROOT_URLCONF = 'parking_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

WSGI_APPLICATION = 'parking_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL SETTINGS
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
   },
   'DEFAULT_AUTO_SCHEMA_CLASS': 'api.custom_schema.ErrorResponseAutoSchema',
   'DEFAULT_MODEL_RENDERING': 'example',
   'DEFAULT_API_URL': 'https://parkonaft.acceleratorpracticum.ru'
}

SITE_NAME = os.getenv(
    'SITE_NAME',
    default='https://parkonaft.acceleratorpracticum.ru'
)
