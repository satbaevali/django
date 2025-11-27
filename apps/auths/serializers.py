from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    EmailField,
    CharField,
    ValidationError
)
from .models import CustomUser
from django.contrib.auth import authenticate




class RegisterSerializer(ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = [
            'email','full_name','password'
        ]
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only = True)
    
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
                    'message':'User not'
                })
            if not user.is_active:
                raise ValidationError({
                    'message':'Error'
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
            'full_name','email','is_active'
        ]