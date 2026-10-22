"""
Feedback modeli: formdan gelen her dilek/şikayet bir kayıt olarak saklanır.
"""
from django.core.validators import RegexValidator
from django.db import models

# Telefon için basit doğrulama: rakam, boşluk, +, -, ( ) karakterleri; 10-20 uzunluk.
# Örn: "0532 123 45 67", "+90 532 123 45 67", "(0532) 123-4567"
phone_validator = RegexValidator(
    regex=r"^\+?[0-9\s\-\(\)]{10,20}$",
    message="Lütfen geçerli bir telefon numarası girin (örn. 0532 123 45 67).",
)


class Feedback(models.Model):
    class Type(models.TextChoices):
        """
        Tür seçenekleri. İlk değer veritabanına yazılır ('dilek'),
        ikinci değer kullanıcıya gösterilir ('Dilek').
        """
        DILEK = "dilek", "Dilek"
        SIKAYET = "sikayet", "Şikayet"

    full_name = models.CharField("Ad Soyad", max_length=120)
    phone_number = models.CharField(
        "Telefon Numarası",
        max_length=20,
        validators=[phone_validator],
    )
    type = models.CharField(
        "Tür",
        max_length=10,
        choices=Type.choices,
    )
    message = models.TextField("Mesaj")
    # auto_now_add: kayıt ilk oluşturulduğunda tarih/saat otomatik atanır, sonra değişmez.
    created_at = models.DateTimeField("Gönderim Tarihi", auto_now_add=True)

    class Meta:
        verbose_name = "Başvuru"
        verbose_name_plural = "Başvurular"
        ordering = ["-created_at"]  # En yeni başvuru en üstte

    def __str__(self):
        return f"{self.full_name} – {self.get_type_display()}"
