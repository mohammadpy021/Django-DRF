from django.urls import path, include

# from .views import ListArticles, DetailArticles
from rest_framework import routers
from blog.api.v1.views import ArticlesViewSet, CategoryViewSet

app_name = "api-v1"

router = routers.SimpleRouter()
router.register("articles", ArticlesViewSet, basename="article")
router.register("category", CategoryViewSet, basename="category")


# urlpatterns = router.urls
urlpatterns = [
    path("", include(router.urls)),
    # path('<int:pk>/', DetailArticles.as_view(), name="article-detail"),
    # path("", ListArticles.as_view(), name="articles-list"),
]
