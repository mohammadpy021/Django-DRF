from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from blog import models
from django.shortcuts import get_object_or_404
from .permissions import AuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .serializers import ArticlesSerializer, CategoriesSerializer
from .paginations import DefaultPagination

# from .filters import ArticleFilter


class ArticlesViewSet(ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = models.Articles.objects.all()
    serializer_class = ArticlesSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = {'categories' :['exact'], 'status':['exact'], 'author' : ['exact']}
    filterset_fields = {
        "categories__title": ["exact", "in"],
        "status": ["exact"],
        "author": ["exact"],
    }
    # filterset_class = ArticleFilter
    search_fields = ["title", "description"]
    ordering_fields = ["id", "created_at"]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
    # def get_serializer_class(self):
    #     if self.request.user.is_staff:
    #         return FullAccountSerializer
    #     return BasicAccountSerializer

    @method_decorator(cache_page(60 * 2))  
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 1))  
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)




class CategoryViewSet(ModelViewSet):
    """
    The GenericViewSet with  `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(60 * 1))  
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    
    
# (generics.GenericAPIView)
# (generics.GenericViewSet) # compatible with routers
# (generics.ApiView)
# (generics.RetrieveUpdateDestroyAPIView)
