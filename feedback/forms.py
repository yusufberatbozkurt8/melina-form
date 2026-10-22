"""
FeedbackForm: kullanıcıdan gelen veriyi doğrular ve modele kaydeder.

ModelForm kullandığımız için alan tipleri ve doğrulayıcılar (ör. telefon
regex'i) doğrudan modelden gelir. Burada yalnızca kullanıcı deneyimini
iyileştiren ek kurallar var.
"""
from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    # Model alanından otomatik üretilen alan "---------" boş seçeneği ekler.
    # Radyo butonlarında bu istenmediği için alanı açıkça tanımlıyoruz.
    type = forms.ChoiceField(
        label="Tür",
        choices=Feedback.Type.choices,
        widget=forms.RadioSelect,
        error_messages={"required": "Lütfen Dilek veya Şikayet seçin."},
    )

    class Meta:
        model = Feedback
        fields = ["full_name", "phone_number", "type", "message"]
        error_messages = {
            "full_name": {"required": "Ad Soyad alanı zorunludur."},
            "phone_number": {"required": "Telefon numarası zorunludur."},
            "message": {"required": "Lütfen mesajınızı yazın."},
        }

    def clean_full_name(self):
        """Fazla boşlukları temizler ve en az iki karakter ister."""
        name = " ".join(self.cleaned_data["full_name"].split())
        if len(name) < 2:
            raise forms.ValidationError("Lütfen adınızı ve soyadınızı girin.")
        return name

    def clean_message(self):
        """Çok kısa (anlamsız) mesajları engeller."""
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Mesajınız en az 10 karakter olmalıdır.")
        return message
