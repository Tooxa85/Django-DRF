from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("lms/", include("Lms.urls", namespace="Lms")),
]
