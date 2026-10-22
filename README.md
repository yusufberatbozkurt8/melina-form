# Dilek & Şikayet Formu (Django + Tailwind + Unfold)

Tek sayfalık, sayfa yenilenmeden gönderilen bir dilek/şikayet formu ve
django-unfold ile modernleştirilmiş bir yönetim paneli.

## Kurulum

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser  # admin paneline giriş için
python manage.py runserver
```

- Form: http://127.0.0.1:8000/
- Yönetim paneli: http://127.0.0.1:8000/admin/

## Dosya yapısı

```
melina_form/
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py      # "unfold" admin'den önce eklendi + UNFOLD ayarları
│   └── urls.py          # /admin/ ve / (form) yönlendirmeleri
├── feedback/
│   ├── models.py        # Feedback modeli (Dilek/Şikayet seçimli)
│   ├── forms.py         # ModelForm + ek doğrulamalar
│   ├── views.py         # AJAX → JSON, normal gönderim → yönlendirme + mesaj
│   ├── urls.py          # feedback:form
│   ├── admin.py         # Unfold ModelAdmin: liste, filtre, arama, rozetler
│   └── apps.py
└── templates/feedback/form.html   # Tailwind CDN ile form + fetch JS
```

## Nasıl çalışır?

1. Kullanıcı formu doldurup "Gönder"e basar.
2. JavaScript formu `fetch` ile `X-Requested-With: XMLHttpRequest` başlığıyla gönderir.
3. View formu doğrular:
   - geçerliyse kaydeder ve `{"ok": true}` döner → form gizlenir, başarı kartı görünür;
   - geçersizse `{"ok": false, "errors": {...}}` döner → hatalar ilgili alanların altında gösterilir.
4. JavaScript kapalıysa form klasik şekilde gönderilir; view kaydedip sayfaya
   geri yönlendirir ve bir başarı mesajı gösterir.

## Admin paneli

- Liste sütunları: Ad Soyad, Telefon, Tür (renkli rozet), Tarih
- Filtreler: Tür (Dilek/Şikayet) ve Tarih
- Arama: Ad Soyad ve telefon numarası
- Üstte tarih gezinmesi (yıl › ay › gün), detay sayfasında bölümlenmiş alanlar
- Kullanıcı ve Grup ekranları da Unfold görünümüne alındı

## Render'da yayınlama

Proje bir Render Blueprint'i (`render.yaml`) içerir:

1. Kodu bir GitHub deposuna gönderin.
2. Render'da **New → Blueprint** seçip depoyu bağlayın.
3. Render `DJANGO_SUPERUSER_PASSWORD` için bir şifre ister: admin paneli şifreniz bu olur
   (kullanıcı adı `admin`).
4. **Apply**'a basın. Render PostgreSQL veritabanını ve web servisini kurar, `build.sh`
   paketleri yükler, statik dosyaları toplar ve tabloları oluşturur.

Not: Site Render Starter (7$/ay) ve PostgreSQL Basic-256mb (6$/ay) planlarında çalışır.

## Canlıya almadan önce (Render dışı)

- `SECRET_KEY` değerini ortam değişkeninden okuyun, `DEBUG = False` yapın,
  `ALLOWED_HOSTS` listesine alan adınızı ekleyin.
- `python manage.py collectstatic` ile statik dosyaları toplayın.
