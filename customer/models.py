# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


COUNTRIES = (('PL', 'Polska'),)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)

        return user


class CustomerUser(AbstractBaseUser, PermissionsMixin):
    country = models.CharField(max_length=50, choices=COUNTRIES)
    street = models.CharField(max_length=60)
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=60)
    email = models.EmailField(blank=False, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(
        max_length=40, blank=True, null=True, unique=False)
    last_name = models.CharField(
        max_length=40, blank=True, null=True, unique=False)
    is_admin = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'auth_user'
