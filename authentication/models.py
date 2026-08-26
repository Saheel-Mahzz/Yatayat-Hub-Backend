from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('first_name','Super')
        extra_fields.setdefault('last_name','Admin')
        extra_fields.setdefault('phone_number','9745328656')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email,password,**extra_fields)    
    

# Create your models here.
class CustomUser(AbstractUser):
    email = models.CharField(unique=True)
    
    phone_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    username = None
    objects = CustomUserManager()
    
class ProfileModel(models.Model):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True)    
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')    
    

    
    # class CustomUserManager(BaseUserManager):
    #     def create_user(self,email,password,**extra_fields):
    #         if  not email:
    #             raise ValueError('Email field must be set!')
    #         email = self.normalize_email('email')
    #         user = self.model() 
