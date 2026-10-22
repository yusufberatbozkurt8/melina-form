"""
Admin paneli ayarları (django-unfold ile).

- Feedback modeli için listeleme, filtreleme, arama ve detay sayfası düzeni.
- User ve Group modelleri de Unfold'un ModelAdmin'i ile yeniden kaydedilir;
  böylece panelin tamamı aynı modern görünüme sahip olur.
"""
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(ModelAdmin):
    # Liste sayfasında görünen sütunlar
    list_display = ("full_name", "phone_number", "show_type", "created_at")
    list_display_links = ("full_name",)

    # Sağ taraftaki filtre paneli: türe ve tarihe göre
    list_filter = ("type", "created_at")

    # Üstteki arama kutusu: isim ve telefona göre
    search_fields = ("full_name", "phone_number")

    # Listenin üstünde yıl > ay > gün şeklinde tarih gezinmesi
    date_hierarchy = "created_at"

    ordering = ("-created_at",)
    list_per_page = 25

    # Başvurular kullanıcıdan geldiği için tarih alanı değiştirilemez
    readonly_fields = ("created_at",)

    # Detay sayfasının bölümleri
    fieldsets = (
        ("Başvuru Sahibi", {"fields": ("full_name", "phone_number")}),
        ("Başvuru", {"fields": ("type", "message")}),
        ("Kayıt Bilgisi", {"fields": ("created_at",)}),
    )

    # Unfold'a özel: Tür sütununu renkli rozet (badge) olarak göster.
    # Dilek -> yeşil, Şikayet -> kırmızı
    @display(
        description="Tür",
        ordering="type",
        label={
            "Dilek": "success",
            "Şikayet": "danger",
        },
    )
    def show_type(self, obj):
        return obj.get_type_display()


# --- Kullanıcı ve Grup ekranlarını da Unfold görünümüne geçir ---
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
