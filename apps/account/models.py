import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.utils.models import BaseModel
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user = self.create_user(email, password, **extra_fields)
        return user

class Address(models.Model):
    """ Basic address information of the user database schema. """

    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        abstract = True

# Create your models here.
class MyUser(AbstractUser, BaseModel,
            Address):
    """ User table schema to store user information.

    User table have basic information of the user
    First name, last name, password are already there as we extended the class AbstractUser. 

    Args:
        AbstractUser (Django's inbuilt class): To override the existing functionality of the user or extend the attributes.
        BaseModel (Abstract Base class): For the common fields like created at ,updated at
        Address (Abstract Base class): For the address information.
    """

    username = None

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=True, db_index=True)
    is_active = models.BooleanField(default=True)
    mobile_no = models.CharField(max_length=15, null=True,blank=True,)
    description = models.TextField(null=True,blank=True)

    objects = UserManager()
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'MyUser'
        verbose_name_plural = 'MyUser'