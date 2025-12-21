#Python modules
from typing import Any


#Django modules
from django.db.models import (
    CharField,
    BooleanField,
    EmailField
)
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.contrib.auth.password_validation import validate_password


#Project modules
from apps.abstracts.models import AbstractBaseModel


class CustomUserManager(BaseUserManager):
    """Custom user manager"""
    
    def __obtain_user_instance(
        self,
        email:str,
        full_name:str,
        password:str,
        **kwargs,
    )->'CustomUser':
        if not email:
            raise ValidationError(
                message="there is not email",
                code="invalid email"
            )
        if not full_name:
            raise ValidationError(
                message= "Not Full name",
                code= "Invalid full name"
            )
        new_user:'CustomUser' = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            password = password,
            **kwargs
        )
        return new_user
    
    #Create user
    def create_user(
        self,
        email:str,
        full_name:str,
        password:str,
        **kwargs:dict[str,Any]
    )->'CustomUser':
        new_user = self.__obtain_user_instance(
            email=email,
            full_name=full_name,
            password=password,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using = self._db)
        return new_user
    
    
    #Create superuser
    
    def create_superuser(
        self,
        email:str,
        full_name:str,
        password:str,
        **kwargs:dict[str,Any]
    )-> 'CustomUser':
        new_user = self.__obtain_user_instance(
            email=email,
            full_name=full_name,
            password=password,
            is_superuser=True,
            is_staff = True,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using = self._db)
        return new_user
    

class CustomUser(AbstractBaseUser,PermissionsMixin,AbstractBaseModel):
    """Custom User model"""
    
    email = EmailField (
        max_length=50,
        verbose_name="Email",
        help_text="Email",
        unique=True,
        db_index=True
    )
    full_name = CharField(
        max_length=100,
        verbose_name="Full name",
        help_text="Full name"
    )
    password = CharField(
        max_length=128,
        validators=[validate_password],
        verbose_name="Password",
        help_text="Password"
    )
    is_active = BooleanField(
        default=True,
        verbose_name="Is_active",
    )
    is_staff = BooleanField(
        default=False,
        verbose_name="Is_staff"
    )
    REQUIRED_FIELDS = ["full_name"]
    USERNAME_FIELD = "email"
    objects = CustomUserManager()
    
    class Meta:
        """Customization of the Model metadata."""
        
        verbose_name="CustomUser"
        verbose_name_plural = "Custom Users"
        ordering = ["-created_at"]

    
    

        


