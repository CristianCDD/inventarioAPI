from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =======================
# Seguridad
# =======================
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)  # ej: inventarioapi-cz62.onrender.com

# =======================
# Apps
# =======================
INSTALLED_APPS = [
    'corsheaders',                 # <--- AÑADIDO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
]

# =======================
# Middleware
# =======================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # <--- PRIMERO
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventario.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'inventario.wsgi.application'

# =======================
# Base de datos
# =======================
DATABASES = {
   'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# =======================
# Passwords
# =======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =======================
# Internacionalización
# =======================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =======================
# Archivos estáticos
# =======================
STATIC_URL = 'static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =======================
# CORS
# =======================
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",   # Live Server
    "http://localhost:5500",
    "http://127.0.0.1:5173",   # Vite
    "http://localhost:5173",
]

# Si usas cookies/autenticación:
# CORS_ALLOW_CREDENTIALS = True
# CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_EXTERNAL_HOSTNAME}"] if RENDER_EXTERNAL_HOSTNAME else []

# Render detrás de proxy (importante en producción)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# =======================
# Config general
# =======================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
