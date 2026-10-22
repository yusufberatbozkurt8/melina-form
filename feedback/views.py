"""
Form sayfasının view'ı.

Aynı view iki şekilde çalışır:
1. AJAX (fetch) isteği  -> JSON döner; sayfa yenilenmeden başarı/hata gösterilir.
2. Normal form gönderimi (JavaScript kapalıysa) -> Post/Redirect/Get deseniyle
   aynı sayfaya yönlendirilir ve bir başarı mesajı gösterilir.
"""
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import FeedbackForm


def _is_ajax(request):
    """İsteğin JavaScript (fetch) ile gönderilip gönderilmediğini kontrol eder."""
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


@require_http_methods(["GET", "HEAD", "POST"])
def feedback_form(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()
            success_text = "Mesajınız bize ulaştı. Teşekkür ederiz!"

            if _is_ajax(request):
                return JsonResponse({"ok": True, "message": success_text})

            messages.success(request, success_text)
            return redirect("feedback:form")

        # Form geçersiz
        if _is_ajax(request):
            # {"alan_adi": ["hata1", ...]} biçiminde hataları döndür
            errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
            return JsonResponse({"ok": False, "errors": errors}, status=400)
        # JS kapalıysa: hatalarla birlikte formu yeniden göster (aşağıya düşer)
    else:
        form = FeedbackForm()

    return render(request, "feedback/form.html", {"form": form})
