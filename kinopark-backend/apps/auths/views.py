from rest_framework.viewsets import ViewSet
from rest_framework import status,permissions
from rest_framework.decorators import action,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import login,logout
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    UserUpdateProfileSerializer,
    ChangePasswordSerializer,
    TokenRefreshResponseSerializer,
    ErrorSerializer,
    AuthResponseSerializer,
    ValidationErrorSerializer,
    MessageSerializer,
    TokenVerifyResponseSerializer
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
@extend_schema_view(
    register=extend_schema(
        summary="User Registration",
        description="Register a new user and returns JWT tokens (access and refresh)",
        tags=['Authentication'],
        request=RegisterSerializer,
        responses={
            201: AuthResponseSerializer,
            400: ValidationErrorSerializer,
        },
        examples=[
            OpenApiExample(
                'Registration Request',
                value={
                    'email': 'user@example.com',
                    'full_name': 'John Doe',
                    'password': 'SecurePass123!',
                    'password2': 'SecurePass123!'
                },
                request_only=True,
                description="Example registration data"
            ),
            OpenApiExample(
                'Successful Registration',
                value={
                    'message': 'Registration was successful',
                    'user': {
                        'id': 1,
                        'full_name': 'John Doe',
                        'email': 'user@example.com',
                        'is_active': True,
                        'created_at': '2024-12-01T10:00:00Z'
                    },
                    'tokens': {
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJh...',
                        'access': 'eyJ0eXAiOiJKV1QiLCJh...'
                    }
                },
                response_only=True,
                status_codes=['201']
            ),
        ]
    ),
    login_user=extend_schema(
        summary="User Login",
        description="Authenticates user and returns JWT tokens",
        tags=['Authentication'],
        request=LoginSerializer,
        responses={
            200: AuthResponseSerializer,
            400: ValidationErrorSerializer,
            401: ErrorSerializer,
        },
        examples=[
            OpenApiExample(
                'Login Request',
                value={
                    'email': 'user@example.com',
                    'password': 'SecurePass123!'
                },
                request_only=True
            ),
            OpenApiExample(
                'Successful Login',
                value={
                    'message': 'Login was successful',
                    'user': {
                        'id': 1,
                        'full_name': 'John Doe',
                        'email': 'user@example.com',
                        'is_active': True,
                        'created_at': '2024-12-01T10:00:00Z'
                    },
                    'tokens': {
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJh...',
                        'access': 'eyJ0eXAiOiJKV1QiLCJh...'
                    }
                },
                response_only=True,
                status_codes=['200']
            ),
        ]
    ),
    logout_user=extend_schema(
        summary="User Logout",
        description="Blacklists the refresh token and logs out the user",
        tags=['Authentication'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'refresh': {'type': 'string', 'description': 'Refresh token to blacklist'}
                },
                'required': ['refresh'],
                'example': {
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJh...'
                }
            }
        },
        responses={
            200: MessageSerializer,
            400: ErrorSerializer,
        },
        examples=[
            OpenApiExample(
                'Logout Request',
                value={'refresh': 'eyJ0eXAiOiJKV1QiLCJh...'},
                request_only=True
            ),
        ]
    ),
    refresh_token=extend_schema(
        summary="Refresh Access Token",
        description="Generate new access token using refresh token",
        tags=['Authentication'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'refresh': {'type': 'string', 'description': 'Refresh token'}
                },
                'required': ['refresh'],
                'example': {
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJh...'
                }
            }
        },
        responses={
            200: TokenRefreshResponseSerializer,
            401: ErrorSerializer,
        },
    ),
    verify_token=extend_schema(
        summary="Verify Token",
        description="Check if the access token is valid",
        tags=['Authentication'],
        responses={
            200: TokenVerifyResponseSerializer,
            401: ErrorSerializer,
        }
    ),
)

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