from django.contrib import admin
from django.urls import path, include
from weather.settings import DEBUG

urlpatterns = [
    path("admin/", admin.site.urls),
    path("data/", include("data.urls")),
    path("users/", include("users.urls")),
]

if DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
