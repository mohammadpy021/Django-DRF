from django.urls import path, include
from .views import ArticleListView, ArticleDetailView

app_name = "blog"
urlpatterns = [
    path("api/v1/", include("blog.api.v1.urls")),
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
]
