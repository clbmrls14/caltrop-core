import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,  PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have a valid email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        superuser = self.create_user(email, password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Game(models.Model):
    """Game with unique ruleset"""
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    track_health = models.BooleanField(default=True)
    players = models.ManyToManyField('Player')

    def __str__(self):
        return self.title


class Player(models.Model):
    """Player in a game"""
    name = models.CharField(max_length=255)
    character_name = models.CharField(max_length=255, blank=True)
    health = models.IntegerField(default=4)

    def __str__(self):
        return self.name
