@echo off
chcp 65001 >nul
title Melina Form - Django
cd /d "%~dp0"

echo.
echo ===============================================
echo   Dilek ^& Sikayet Formu - kurulum ve baslatma
echo ===============================================
echo.

rem --- Python'u bul (once Anaconda, sonra sistem Python'u) ---
set "PY="
if exist "%USERPROFILE%\anaconda3\python.exe" set "PY=%USERPROFILE%\anaconda3\python.exe"
if not defined PY (
  where py >nul 2>nul && set "PY=py"
)
if not defined PY (
  where python >nul 2>nul && set "PY=python"
)
if not defined PY (
  echo [HATA] Python bulunamadi. python.org adresinden Python kurup tekrar deneyin.
  pause
  exit /b 1
)
echo Python: %PY%

rem --- Sanal ortam (ilk calistirmada olusturulur) ---
if not exist "venv\Scripts\python.exe" (
  echo.
  echo [1/4] Sanal ortam olusturuluyor...
  "%PY%" -m venv venv || goto :hata
)
set "VPY=venv\Scripts\python.exe"

echo.
echo [2/4] Paketler kuruluyor (Django, django-unfold)...
"%VPY%" -m pip install --disable-pip-version-check -q -r requirements.txt || goto :hata

echo.
echo [3/4] Veritabani hazirlaniyor...
"%VPY%" manage.py migrate || goto :hata

rem --- Yerel test icin admin kullanicisi (zaten varsa atlanir) ---
set "DJANGO_SUPERUSER_USERNAME=admin"
set "DJANGO_SUPERUSER_EMAIL=admin@example.com"
set "DJANGO_SUPERUSER_PASSWORD=Admin12345!"
"%VPY%" manage.py createsuperuser --noinput >nul 2>nul

echo.
echo [4/4] Sunucu baslatiliyor...
echo.
echo   Form ............ http://127.0.0.1:8000/
echo   Yonetim paneli .. http://127.0.0.1:8000/admin/
echo   Giris: kullanici adi "admin", sifre "Admin12345!"
echo.
echo   Kapatmak icin bu pencerede CTRL+C'ye basin.
echo.
start "" cmd /c "timeout /t 4 >nul & start http://127.0.0.1:8000/"
"%VPY%" manage.py runserver
pause
exit /b 0

:hata
echo.
echo [HATA] Bir adim basarisiz oldu. Bu pencerenin ekran goruntusunu Claude'a gonderin.
pause
exit /b 1
