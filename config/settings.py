"""
Proje ayarları.

Önemli noktalar:
- "unfold" uygulaması, "django.contrib.admin"den ÖNCE eklenmelidir; aksi halde
  admin şablonları Unfold'un şablonlarını ezer ve tasarım uygulanmaz.
- UNFOLD sözlüğü admin panelinin başlığını, ikonunu ve yan menüsünü belirler.
"""
import os
from pathlib import Path

import dj_database_url
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

# Canlıda (Render) bu değerler ortam değişkenlerinden gelir; yerelde varsayılanlar kullanılır.
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-yalnizca-yerel-gelistirme-icin"
)
DEBUG = os.environ.get("DEBUG", "1") == "1"

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = []

# Render, sitenin adresini bu değişkenle verir (ör. melina-form.onrender.com)
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

if not DEBUG:
    # Render HTTPS'i önündeki proxy'de sonlandırır
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    # --- Unfold: admin'den önce gelmeli ---
    "unfold",
    # --- Django çekirdek uygulamaları ---
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # --- Bizim uygulamamız ---
    "feedback",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Statik dosyaları canlıda sunar
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # Admin'in Türkçe görünmesi için
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Proje düzeyindeki şablon klasörü
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# DATABASE_URL tanımlıysa (Render PostgreSQL) onu, değilse yerel SQLite'ı kullan
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Dil ve saat dilimi ---
LANGUAGE_CODE = "tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Unfold admin teması ayarları ---
UNFOLD = {
    "SITE_TITLE": "Dilek & Şikayet Paneli",       # Tarayıcı sekmesindeki başlık
    "SITE_HEADER": "Dilek & Şikayet",             # Sol üstteki başlık
    "SITE_SYMBOL": "forum",                       # Material Symbols ikon adı
    "SHOW_HISTORY": True,                         # Kayıt geçmişi butonu
    "SHOW_VIEW_ON_SITE": False,
    "SIDEBAR": {
        "show_search": True,                      # Menüde arama kutusu
        "show_all_applications": True,            # "Tüm uygulamalar" açılır listesi
        "navigation": [
            {
                "title": "Başvurular",
                "separator": True,
                "items": [
                    {
                        "title": "Tüm Başvurular",
                        "icon": "inbox",
                        "link": reverse_lazy("admin:feedback_feedback_changelist"),
                    },
                ],
            },
            {
                "title": "Yönetim",
                "separator": True,
                "items": [
                    {
                        "title": "Kullanıcılar",
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": "Gruplar",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}
