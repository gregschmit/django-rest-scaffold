from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("api/", include("autorest.api_urls")),
    path("example/", views.ExampleView.as_view()),
    path("admin/", admin.site.urls),
]
