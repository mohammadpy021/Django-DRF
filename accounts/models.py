from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        email = self.normalize_email(email)
        user = self.model( email=email, **extra_fields)
        user.password = make_password(password)
        # user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        # super(self).create_superuser(self, username, email=None, password=None, **extra_fields)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # extra_fields.setdefault("is_verified", True)#custom

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_verified") is not True:#custom
            raise ValueError("Superuser must have is_verified=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    '''
    Custom user 
    '''
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(("verified"),
        default=False,
        help_text=("user verification by email"),)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email
# def set_username(sender, instance, **kwargs):
#     if not instance.username:
#         instance.username = instance.email.split('@')[0]
# models.signals.pre_save.connect(set_username, sender=User)



@receiver(post_save, sender=User) 
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(pre_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    try:
        instance.profile.delete()
    except Profile.DoesNotExist:
        pass