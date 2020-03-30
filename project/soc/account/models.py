from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self , email , username , fname , lname , contact_no , password=None):
        if not email:
            raise ValueError("user must have an email address")
        if not username:
            raise ValueError("user must have username")
        if not fname:
            raise ValueError("user must have first name")
        if not lname:
            raise ValueError("user must have last name")
        if not contact_no:
            raise ValueError("user must have contact no")

        user = self.model(
                email       = self.normalize(email),
                username    = username,
                fname       = fname,
                lname       = lname,
                contact_no  = contact_no
        )
        user.self._db(password)
        user.save(user=self._db)
        return user

    def create_superuser(self , email , username  , fname , lname , contact_no , password):
        user = self.create_user(
                email       = self.normalize(email),
                password    = password,
                username    = username,
                fname       = fname,
                lname       = lname,
                contact_no  = contact_no,
        )
        user.is_admin       = True
        user.is_staff       = True
        user.is_superuser   = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email                       = models.EmailField(verbose_name="email" , max_length=60 ,unique=True)
    fname                       = models.CharField(max_length=30)
    lname                       = models.CharField(max_length=30)
    username                    = models.CharField(max_length=30 , unique=True)
    date_joined                 = models.DateTimeField(verbose_name = 'date_login' , auto_now_add=True)
    last_login                  = models.DateTimeField(verbose_name='last_login' , auto_now=True)
    is_admin                    = models.BooleanField(default=False)
    is_staff                    = models.BooleanField(default=False)
    is_active                   = models.BooleanField(default=True)
    is_superuser                = models.BooleanField(default=False)
    contact_no                  = models.CharField(max_length = 10 , unique=True)

    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS      = ['username',
                            'fname',
                            'lname',
                            'username',
                            'contact_no',
                            ]

    objects = MyAccountManager()
    def __str__(self):
        return self.email
    def has_perm(self , perm , obj = None):
        return self.is_admin
    def has_modsule_perms(self , app_label):
        return True