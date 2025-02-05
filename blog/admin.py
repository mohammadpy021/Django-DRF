from django.contrib import admin
from .models import Articles, Category


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["title"],
    }
    list_display = ("title", "status", "slug","author", "get_categories")

    def get_categories(self, obj):
        return [str(i) for i in obj.categories.all()]
    get_categories.short_description = 'دسته بندی'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["title"],
    }
    list_display = ("title", "slug", "status")
