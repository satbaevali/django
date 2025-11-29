from rest_framework.viewsets import ViewSet
from rest_framework import status,permissions
from rest_framework.decorators import action,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import login

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer
)

from .models import CustomUser


class RegisterView(ViewSet):
    permission_classes = [permissions.AllowAny]
    def create(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            },status=status.HTTP_201_CREATED)


class LoginView(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self,request):
        serializer = LoginSerializer(data = request.data,)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        login(request,user)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh':str(refresh),
            'access':str(refresh.access_token),
            'message':'Login succsefelly'
        },status=status.HTTP_200_OK)
        
        
class UserProfileView(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def list(self,request):
        users = CustomUser.objects.all()
        serializer = UserProfileSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
    def retrieve(self,request,pk=None):
        user = CustomUser.objects.get(pk = pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)