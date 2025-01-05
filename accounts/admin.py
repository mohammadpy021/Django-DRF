from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

    

        
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_superuser", "is_active","is_verified")
    list_filter = ("email", "is_superuser", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active","is_verified", "groups", "user_permissions")}),
        ("Important date", {
            "fields": (
                "last_login",
                )
            }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active","is_superuser", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass





