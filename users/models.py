# from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    # def create_superuser(self, email, password, **extra_fields):
    #     """Create and save a SuperUser with the given email and password."""
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')

    #     return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    pass
    """User model."""
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=False, null=True)
    last_name = models.CharField(max_length=30, blank=False, null=True)
    email = models.EmailField(unique=True, blank=False, null=True)
    username = models.CharField(max_length=20, blank=False, null=True)
    password = models.CharField(max_length=15, blank=False, null=True)

    work_position = models.CharField(max_length=30, blank=False, null=True)
    short_bio = models.CharField(max_length=100, blank=False, null=True)
    social_link_github = models.URLField(null=True, blank=True)
    social_link_linkedIn = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True, unique=True, editable=False)

    def __str__(self) -> str:
        return self.email

    class Meta:
        ordering = ['id']


class Skill(models.Model):
    owner = models.ForeignKey(Developer, on_delete=models.CASCADE, null=False)
    description = models.CharField(null=True, max_length=20, blank=False)
    id = models.AutoField(primary_key=True, unique=True, editable=False)

    def __str__(self) -> str:
        return self.description

    class Meta:
        ordering = ['id']


class Message(models.Model):
    sender = models.ForeignKey(Developer, on_delete=models.CASCADE, null=True)
    recipient = models.ForeignKey(
        Developer, on_delete=models.CASCADE, null=True, related_name='messages')

    subject = models.CharField(max_length=50, null=True, blank=False)
    content = models.CharField(max_length=500, null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, null=True)

    id = models.AutoField(primary_key=True, unique=True, editable=False)

    def __str__(self) -> str:
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']

    
# class EmailBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:  # to allow authentication through phone number or any other field, modify the below statement
#             user = UserModel.objects.get(email__iexact=email)
#         except UserModel.DoesNotExist:
#             UserModel().set_password(password)
#         # except MultipleObjectsReturned:
#         #     return User.objects.filter(email=username).order_by('id').first()
#         else:
#             if user.check_password(password) and self.user_can_authenticate(user):
#                 return user

#     def get_user(self, user_id):
#         try:
#             user = UserModel.objects.get(pk=user_id)
#         except UserModel.DoesNotExist:
#             return None

#         return user if self.user_can_authenticate(user) else None
