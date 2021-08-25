from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
                email = self.normalize_email(email),
                username = username,
            )

        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
                email = self.normalize_email(email),
                username = username,
                password = password
            )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email           = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username        = models.CharField(verbose_name='username', max_length=20, unique=True)
    phone_number    = models.CharField(max_length=14, help_text="Enter phone number with country code")
    date_joined     = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    remember_me     = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class VerificationCode(models.Model):
    number = models.CharField(max_length=5, blank=True)
    user = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        number_list = [0,1,2,3,4,5,6,7,8,9]
        code_items = []

        for i in range(6):
            num = random.choice(number_list)
            code_items.append(num)
        
        code_string = "".join(str(item) for item in code_items)
        self.number = code_string
        
        super().save(*args, **kwargs)