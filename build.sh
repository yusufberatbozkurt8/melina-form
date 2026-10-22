#!/usr/bin/env bash
# Render her dağıtımda bu betiği çalıştırır.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Admin kullanıcısını oluştur (zaten varsa hata yok sayılır)
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --noinput || true
fi
