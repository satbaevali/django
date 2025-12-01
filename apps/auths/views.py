from rest_framework.viewsets import ViewSet
from rest_framework import status,permissions
from rest_framework.decorators import action,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import login,logout
from django.shortcuts import get_object_or_404

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    UserUpdateProfileSerializer,
    ChangePasswordSerializer
)

from .models import CustomUser


'''class RegisterView(ViewSet):
    """Register View"""
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
    
'''
class AuthViewSet(ViewSet):
    """Authentication ViewSet"""
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False,methods=['post'],url_path='register')
    def register(self,request):
        """Регистрация пользователя"""
        serializer = RegisterSerializer(data = request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message':'Registration was successful',
                'user':UserProfileSerializer(user).data,
                'tokens':{
                    'refresh':str(refresh),
                    'access':str(refresh.access_token)
                }
            },status=status.HTTP_201_CREATED)
        return Response({
            'error': serializer.errors,
            
        },status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(detail=False,methods=['post'], url_path='login')
    def login(self,request):
        """  Вход пользователя"""
        serializer = LoginSerializer(data = request.data , context = {'request':request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            login(request,user)
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message':"Login was successful",
                'user':UserProfileSerializer(user).data,
                'tokens':{
                    'refresh':str(refresh),
                    'access':str(refresh.access_token)
                }
            })
        return Response({
            'error':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False, methods=['post'],url_path='logout', permission_classes = [permissions.IsAuthenticated])
    def logout_view(self,request):
        """Выход пользователя"""
        try:
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                raise ValueError({
                    'error':'There is not refresh token'
               },status = status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            logout(request)
            
            return Response({
                'message':"Logout is successful"
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error':f'Exit error {str(e)}'
            },status = status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False, methods=['post'], url_path='refresh')
    def refresh_token(self, request):
        """
        Обновление access токена
        """
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
                'message': 'Token refreshed successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid or expired refresh token'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    
    @action(detail=False, methods=['get'], url_path='verify', permission_classes=[permissions.IsAuthenticated])
    def verify_token(self, request):
        """
        Проверка валидности токена
        """
        return Response({
            'valid': True,
            'user': UserProfileSerializer(request.user).data
        }, status=status.HTTP_200_OK)
        

class UserViewSet(ViewSet):
    """User Profile ViewSet"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self,request):
        """Список всех пользователей (только для staff)"""
        
        if not request.user.is_staff:
            return Response({
                'error': 'You do not have permission to view users list'
            }, status=status.HTTP_403_FORBIDDEN)
        
        user = CustomUser.objects.all()
        serilaizer = UserProfileSerializer(user,many = True)
        
        return Response({
            'count':user.count(),
            'result':serilaizer.data
        },status=status.HTTP_200_OK)
        
    
    def retreive(self,request,pk=None):
        
        """Получить пользователя по ID"""
        
        if not request.user.is_staff and str(request.user.id) != pk:
            return Response({
                'error': 'You do not have permission to view this profile'
            }, status=status.HTTP_403_FORBIDDEN)
        
        user = get_object_or_404(CustomUser,pk = pk)
        serilizer = UserProfileSerializer(user)
        
        return Response(
            serilizer.data,status=status.HTTP_200_OK
        )
        
        
    @action(detail=False, methods=['get'], url_path='me')
    def current_user(self,request):
        """Current user"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    @action(detail=False, methods=['put','putch'],url_path='me/update')
    def update_profile(self,request):

        serializer = UserUpdateProfileSerializer(
            request.user,
            data = request.data,
            partial = request.method == "Putch"
        )
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'message':"Updated user profile",
                'result':UserProfileSerializer(request.user).data
            },status=status.HTTP_201_CREATED)
    
        
    @action(detail=False, methods=['post'], url_path='change_password')
    def change_password(self,request):
        serializer = ChangePasswordSerializer(
            data = request.data,
            context = {'request':request}
        )
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
        
        refresh = RefreshToken.for_user(request.user)
        
        return Response({
            'message':"Password changed successfully ",
            'tokens':{
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            }
        },status=status.HTTP_200_OK)
    
    
    @action(detail=False, methods=['post'],url_path='deactivate')
    def deactivate_user(self,request):
        
        password = request.data.get('password')
        
        if not password:
            return Response({
                'error':'Password is required to deactivate account'
            },status=status.HTTP_400_BAD_REQUEST)
        if not request.user.check_password(password):
            return Response({
                'error': 'Invalid password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.is_active = False
        request.user.save()
        
        return Response({
            'message': 'Account deactivated successfully'
        }, status=status.HTTP_200_OK)
        
        
    @action(detail=False, methods=['post'],url_path='delete')
    def delete_account(self,request):
        
        password = request.data.get('password')
        confirm = request.data.get('confirm')
        
        if not password or confirm != 'DELETE':
            return Response({
                'error': 'Password and confirmation "DELETE" are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.check_password(password):
            return Response({
                'error': 'Invalid password'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        user_email = request.user.email
        request.user.delete()
        
        return Response({
            'message': f'Account {user_email} deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)