from crum import get_current_user
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_superuser=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class InnerHealthAbstractClass(models.Model):
    class Meta:
        verbose_name = "InnerHealth Abstract Class"
        abstract = True

    is_active = models.BooleanField(
        default=True,
        verbose_name=("Is active")
    )
    created = models.DateField(
        auto_now=True,
        verbose_name=("Created")
    )
    updated = models.DateField(
        auto_now=True,
        verbose_name=("Updated")
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="+",
        verbose_name=("Updated By")
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="+",
        verbose_name=("Updated By")
    )

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.updated_by = user

        super(InnerHealthAbstractClass, self).save(*args, **kwargs)

    def delete(self):
        self.is_active = False
        self.save()


class Profile(InnerHealthAbstractClass):
    class Meta:
        verbose_name = "Profile Abstract Class"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=("User")
    )
