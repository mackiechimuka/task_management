from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,Group, Permission
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set.')
        
        if not password:
            raise ValueError("The password must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email =models.EmailField(unique=True)
    username =None
    groups = models.ManyToManyField(Group, blank=True, related_name='user_set_custom')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='user_set_custom')


    USERNAME_FIELD ='email'
    REQUIRED_FIELDS =[]
     
    objects= UserManager()

