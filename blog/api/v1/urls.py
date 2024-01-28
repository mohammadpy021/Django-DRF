from django.urls import path, include
from .views import ListArticles, DetailArticles

app_name = "api-v1"
urlpatterns = [
    path("", ListArticles.as_view(), name="articles-list"),
    path('<int:pk>/', DetailArticles.as_view(), name="articles-detail"),
]
