from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='электронная почта')

    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', null=True, blank=True)
    phone = models.CharField(max_length=35, verbose_name='номер телефона', null=True, blank=True)
    country = models.CharField(max_length=50, verbose_name='страна', null=True, blank=True)

    verification_key = models.CharField(max_length=50, verbose_name='ключ верификации', null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name='верифицирован')


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
