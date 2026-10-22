"""
feedback uygulamasının URL'leri.

app_name sayesinde URL'lere "feedback:form" şeklinde isimle erişilir
(ör. redirect("feedback:form") veya şablonda {% url 'feedback:form' %}).
"""
from django.urls import path

from . import views

app_name = "feedback"

urlpatterns = [
    path("", views.feedback_form, name="form"),
]
