from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"
    verbose_name = "Dilek ve Şikayetler"  # Admin menüsünde görünen uygulama adı
