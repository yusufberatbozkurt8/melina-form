"""
Proje düzeyindeki URL yönlendirmeleri.

- /admin/  -> Unfold temalı Django admin paneli
- /        -> feedback uygulamasının formu (feedback/urls.py)
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("feedback.urls")),
]
