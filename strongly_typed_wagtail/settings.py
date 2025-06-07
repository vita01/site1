import os
from pathlib import Path
from dotenv import load_dotenv
from decouple import config

load_dotenv()

#OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_API_KEY='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'
BOT_REFERERS = os.getenv("BOT_REFERERS", "http://localhost:8000").split(",")
OPENROUTER_MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

#SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '14271997Vika')

#DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ['true', '1', 'yes']

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'love2self.com',
    'www.love2self.com',
    'site1-8kn8.onrender.com',
]
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]

print("ALLOWED_HOSTS:", ALLOWED_HOSTS)
print("DJANGO_SETTINGS_MODULE:", os.getenv('DJANGO_SETTINGS_MODULE'))

INSTALLED_APPS = [
    "home",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = "strongly_typed_wagtail.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "strongly_typed_wagtail.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
#STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = "/media/"
#MEDIA_ROOT = BASE_DIR / "media"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
WAGTAIL_SITE_NAME = "Strongly Typed"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
