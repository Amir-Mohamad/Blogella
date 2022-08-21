from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from PIL import Image


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **other_fields):
        if username is None:
            raise TypeError("Users should have a username")
        if email is None:
            raise TypeError("Users should have a Email")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **other_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            **other_fields,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)
        return user


AUTH_PROVIDERS = {
    "facebook": "facebook",
    "google": "google",
    "twitter": "twitter",
    "email": "email",
}


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get("email")
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="media/default.png", upload_to="profile_pics")
    special_user = models.DateTimeField(default=timezone.now)

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False

    is_special_user.boolean = True

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)  # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)  # Resize image
            # Save it again and override the larger image
            img.save(self.image.path)
