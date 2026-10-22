import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120, verbose_name="Ad Soyad")),
                (
                    "phone_number",
                    models.CharField(
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Lütfen geçerli bir telefon numarası girin (örn. 0532 123 45 67).",
                                regex="^\\+?[0-9\\s\\-\\(\\)]{10,20}$",
                            )
                        ],
                        verbose_name="Telefon Numarası",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("dilek", "Dilek"), ("sikayet", "Şikayet")],
                        max_length=10,
                        verbose_name="Tür",
                    ),
                ),
                ("message", models.TextField(verbose_name="Mesaj")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Gönderim Tarihi")),
            ],
            options={
                "verbose_name": "Başvuru",
                "verbose_name_plural": "Başvurular",
                "ordering": ["-created_at"],
            },
        ),
    ]
