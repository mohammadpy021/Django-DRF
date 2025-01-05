from django_filters import rest_framework as filters
from blog.models import Articles, Category
import django_filters


# class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
#     pass


# class ArticleFilter(filters.FilterSet):
#     # min_price = filters.NumberFilter(field_name="categories", lookup_expr='gte')
#     # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
#     # categories__in = django_filters.ChoiceFilter(field_name="categories")
#     # category = NumberInFilter(field_name='categories__id', lookup_expr='in')
#     # category = django_filters.Filter(field_name="categories", lookup_expr='in')
#     # category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

#     class Meta:
#         model = Articles
#         fields = {
#             # 'categories': ['exact', 'in'],
#             'author': ['exact'],
#         }

# class ArticleFilter(django_filters.FilterSet):
#     # author   = django_filters.CharFilter(lookup_expr="exact", field_name='author')
#     categories = django_filters.CharFilter(method='filter_category')

#     class Meta:
#         model = Articles
#         fields = ['author', 'categories']

#     def filter_category(self, queryset, name, value):
#         category = value.split(',')
#         return queryset.filter(categories__title__iexact=category)
