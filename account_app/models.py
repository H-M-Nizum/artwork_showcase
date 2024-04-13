from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager

#  Custom User Model
class ArtistModel(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)  
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=200)
    bio = models.TextField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname', 'email', 'bio']


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class ArtworkModel(models.Model):
    artist = models.ForeignKey(ArtistModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()

    def __str__(self):
        return self.title

