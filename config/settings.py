import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8l8o(-2su$6t%k424293i#x672q0$*^itfyi9r32$8j-igo7zf'

DEBUG = True

ALLOWED_HOSTS = []

# ✅ APPS INSTALADOS - ORGANIZADOS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cadastro.apps.CadastroConfig',

    # SEUS APPS
    'accounts',      # App de usuários
    'relatos',       # App de relatos
    'ong',           # App de ONGs
    'conteudos',     # App de conteúdos
    'eventos',       # App de eventos
    'ajuda',         # App de ajuda
    'core',          # App core
       
    # EXTRAS
    'widget_tweaks',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'config.wsgi.application'

# ✅ DATABASE POSTGRESQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'uniraros_infog',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ✅ CONFIGURAÇÕES DE AUTENTICAÇÃO (CORRIGIDAS)
AUTH_USER_MODEL = 'accounts.CustomUser'  # ✅ CORRIGIDO: CustomUser

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.StatusBackend',  # ✅ Backend customizado
]

# ✅ URLs DE LOGIN
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'  # ✅ Vai para a página inicial
LOGOUT_REDIRECT_URL = '/'  # ✅ Vai para a página inicial

# ✅ CONFIGURAÇÕES DE EMAIL GMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sistemaunirarosinfog25@gmail.com'
EMAIL_HOST_PASSWORD = 'nhtr ekwb ndkn gxrv'
DEFAULT_FROM_EMAIL = 'Sistema Doenças Raras <sistemaunirarosinfog25@gmail.com>'
SITE_URL = 'http://localhost:8000'

# ✅ EMAILS DOS ADMINISTRADORES
ADMIN_EMAILS = [
    'sistemaunirarosinfog25@gmail.com' 
]

# ✅ VALIDAÇÕES DE SENHA (ADICIONANDO NOSSA VALIDAÇÃO CUSTOMIZADA)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'accounts.validators.PasswordValidator',  # ✅ NOSSO VALIDADOR
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # ✅ Compatível com nossa validação
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ✅ CONFIGURAÇÕES INTERNACIONAIS
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ✅ ARQUIVOS ESTÁTICOS
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",  # ✅ Pasta static global se tiver
]

# ✅ MIDIA FILES (se usar uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'