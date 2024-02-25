from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ArticlesSerializer, CategoriesSerializer
from rest_framework.permissions import IsAuthenticated
from blog import models
from django.shortcuts import  get_object_or_404
from rest_framework import generics, viewsets
from .permissions import AuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination
# from .filters import ArticleFilter
'''
class ListArticles(APIView):
    """ articles with APIView"""
    permission_classes = [IsAuthenticated]
    serializer_class  = ArticlesSerializer
    
    def get(self, request, format=None):
        articles = models.Articles.objects.all()
        serializer = self.serializer_class(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
'''

'''
class ListArticles(generics.ListCreateAPIView):
    """ list of articles using generics """ 
    queryset = models.Articles.objects.all()
    serializer_class   = ArticlesSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = {'categories' :['exact'], 'status':['exact'], 'author' : ['exact']}
    filterset_fields = {'categories__title' :['exact', 'in'], 'status':['exact'], 'author' : ['exact']}
    # filterset_class = ArticleFilter
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'created_at']

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
    # def get_serializer_class(self):
    #     if self.request.user.is_staff:
    #         return FullAccountSerializer
    #     return BasicAccountSerializer
'''

class ArticlesViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.Articles.objects.all()
    serializer_class   = ArticlesSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = {'categories' :['exact'], 'status':['exact'], 'author' : ['exact']}
    filterset_fields = {'categories__title' :['exact', 'in'], 'status':['exact'], 'author' : ['exact']}
    # filterset_class = ArticleFilter
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'created_at']

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
    # def get_serializer_class(self):
    #     if self.request.user.is_staff:
    #         return FullAccountSerializer
    #     return BasicAccountSerializer




''' 
class DetailArticles(generics.GenericAPIView):
 
    permission_classes = [IsAuthenticated]
    serializer_class  = ArticlesSerializer
    queryset = models.Articles.objects.all()
    # lookup_field = "slug"                 # set path('<slug:slug>/') in the urls
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        
    #generics.ApiViews
    # def get(self, request, pk):
    #     articles = get_object_or_404(models.Articles, pk=pk)
    #     serializer = self.serializer_class(articles)
    #     return Response(serializer.data)
'''

'''
class DetailArticles(generics.RetrieveUpdateDestroyAPIView):
    """detail of articles using generic """
    queryset = models.Articles.objects.all()
    serializer_class   = ArticlesSerializer
    permission_classes = [AuthorOrReadOnly]
'''

class CategoryViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = models.Category.objects.all()
    serializer_class   = CategoriesSerializer
    permission_classes = [IsAuthenticated]
