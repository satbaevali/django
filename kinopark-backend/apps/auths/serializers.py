from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    EmailField,
    CharField,
    ValidationError
)
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password 


class RegisterSerializer(ModelSerializer):
    password = CharField(
        write_only = True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = CharField(
        write_only = True,
        required=True,
        style={'input_type': 'password'},
        label="Подтверждение пароля"
    )
    
    
    class Meta:
        model = CustomUser
        fields = [
            'email','full_name','password','password2'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True}
        }
    
    
    def validate_email(self,value):
        "Unique email"
        if CustomUser.objects.filter(email = value.lower()).exists():
            raise ValidationError("the User with this email already exists")
        return value.lower()
    
    
    def validate_full_name(self,value):
        if len(value.strip()) < 2:
            raise ValidationError('The full name must contain at least 2 characters')
        if not any(char.isalpha() for char in value):
            raise ValidationError('Name must contain letters')
        return value.strip()
          
            
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({
                'password2':"Not correct"
            })
        return attrs
    
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()
        return user
    

class LoginSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only = True)
    
    
    def validate_email(self,value):
        return value.lower().strip()
    
    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            
            user = authenticate(
                request=self.context.get('request'),
                username = email,
                password = password
            )
            if not user:
                raise ValidationError({
                    'message':'There is User not '
                })
            if not user.is_active:
                raise ValidationError({
                    'message':'User is a deactivate'
                })
            attrs['user'] = user
            return attrs
        else:
            raise ValidationError({
                'message':'Error not email or not password'
            })
        
        
class UserProfileSerializer(ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = [
            'full_name','email','is_active','created_at'
        ]
        read_only_fields = ['id', 'email', 'is_active', 'created_at']
        

class UserUpdateProfileSerializer(ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['full_name']
        
    
    def validate_full_name(self,value):
        if len(value.strip()) < 2:
            raise ValidationError({
                'detail':'The full name must contain at least 2 characters'
            })
        return value.strip()
    
    
class ChangePasswordSerializer(Serializer):
    old_password =CharField(
        write_only = True,
        required = True
    )
    new_password = CharField(
        write_only = True,
        validators = [validate_password]
    )
    new_password2 = CharField(
        write_only = True,
        required = True
    )
    
    def validate_old_password(self,value):
        user = self.context['request'].user
        
        if not user.check_password(value):
            raise ValidationError(
                'Old password is not correct'
            )
        return value
    
    
    def validate_new_password(self,value):
        user = self.context['request'].user
        
        if user.check_password(value):
            raise ValidationError({
                'detail':"The new password must be different from the old one."
            })
        return value
    
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise ValidationError({
                'new_password2':"The new passwords don match"
            })
        return attrs
    
    
class TokenSerializer(Serializer):
    """JWT Tokens"""
    refresh = CharField(help_text="JWT refresh token")
    access = CharField(help_text="JWT access token")


class AuthResponseSerializer(Serializer):
    """Authentication response with tokens"""
    message = CharField(help_text="Success message")
    user = UserProfileSerializer(help_text="User profile data")
    tokens = TokenSerializer(help_text="JWT tokens")


class ErrorSerializer(Serializer):
    """Error response"""
    error = CharField(help_text="Error message")


class ValidationErrorSerializer(Serializer):
    """Validation error response"""
    errors = CharField(help_text="Validation errors")


class MessageSerializer(Serializer):
    """Simple message response"""
    message = CharField(help_text="Response message")


class TokenRefreshResponseSerializer(Serializer):
    """Token refresh response"""
    access = CharField(help_text="New JWT access token")
    message = CharField(help_text="Success message")


class TokenVerifyResponseSerializer(Serializer):
    """Token verification response"""
    valid = CharField(help_text="Token validity status")
    user = UserProfileSerializer(help_text="User data")


class PasswordChangeResponseSerializer(Serializer):
    """Password change response"""
    message = CharField(help_text="Success message")
    tokens = TokenSerializer(help_text="New JWT tokens after password change")


class ProfileUpdateResponseSerializer(Serializer):
    """Profile update response"""
    message = CharField(help_text="Success message")
    user = UserProfileSerializer(help_text="Updated user data")
