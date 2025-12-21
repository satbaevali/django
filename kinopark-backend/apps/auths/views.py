#Python modules
from drf_spectacular.utils import(
    extend_schema_view,
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiTypes
)    
from rest_framework_simplejwt.tokens import RefreshToken


#Django REST Freamework modules
from rest_framework.viewsets import ViewSet
from rest_framework import status,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import login,logout
from django.shortcuts import get_object_or_404
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT
)


#Project modules
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
from auths.permissions import IsOwnerOrReadOnly



@extend_schema_view(
    register=extend_schema(
        summary="User Registration",
        description="Register a new user and returns JWT tokens (access and refresh)",
        tags=['Authentication'],
        request=RegisterSerializer,
        responses={
            HTTP_201_CREATED: AuthResponseSerializer,
            HTTP_400_BAD_REQUEST: ValidationErrorSerializer,
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
            HTTP_200_OK: AuthResponseSerializer,
            HTTP_400_BAD_REQUEST: ValidationErrorSerializer,
            HTTP_401_UNAUTHORIZED: ErrorSerializer,
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
            HTTP_200_OK: MessageSerializer,
            HTTP_400_BAD_REQUEST: ErrorSerializer,
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
            HTTP_200_OK: TokenRefreshResponseSerializer,
            HTTP_401_UNAUTHORIZED: ErrorSerializer,
        },
    ),
    verify_token=extend_schema(
        summary="Verify Token",
        description="Check if the access token is valid",
        tags=['Authentication'],
        responses={
            HTTP_200_OK: TokenVerifyResponseSerializer,
            HTTP_401_UNAUTHORIZED: ErrorSerializer,
        }
    ),
)

class AuthViewSet(ViewSet):
    """Authentication ViewSet"""
    
    
    permission_classes = [permissions.AllowAny]
    
    
    @action(detail=False,methods=['post'],url_path='register')
    def register(self,request):
        """Registration of the user"""
        
        
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
        """User Login"""
        
        
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
        """Logout user by blacklisting the refresh token"""
        
        
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
        Refresh JWT access token using the provided refresh token
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
        Verify JWT token validity
        """
        return Response({
            'valid': True,
            'user': UserProfileSerializer(request.user).data
        }, status=status.HTTP_200_OK)
        


@extend_schema_view(
    list=extend_schema(
        summary="List Users",
        description="Retrieve a list of all users in the system. Only accessible by staff members.",
        tags=['Users'],
        responses={
            HTTP_200_OK: OpenApiResponse(
                response=UserProfileSerializer(many=True),
                description="Successfully retrieved users list",
                examples=[
                    OpenApiExample(
                        'Successful Response',
                        value={
                            'count': 2,
                            'result': [
                                {
                                    'id': 1,
                                    'full_name': 'John Doe',
                                    'email': 'john.doe@example.com',
                                    'is_active': True,
                                    'created_at': '2024-12-01T10:00:00Z'
                                },
                                {
                                    'id': 2,
                                    'full_name': 'Jane Smith',
                                    'email': 'jane.smith@example.com',
                                    'is_active': True,
                                    'created_at': '2024-12-02T12:30:00Z'
                                }
                            ]
                        },
                        response_only=True,
                    )
                ]
            ),
            HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorSerializer,
                description="User does not have staff permissions",
                examples=[
                    OpenApiExample(
                        'Permission Denied',
                        value={
                            'error': 'You do not have permission to view users list'
                        },
                        response_only=True,
                    )
                ]
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve User Profile",
        description="Get detailed information about a specific user by ID. Staff can view any profile, regular users can only view their own.",
        tags=['Users'],
        responses={
            HTTP_200_OK: OpenApiResponse(
                response=UserProfileSerializer,
                description="Successfully retrieved user profile",
                examples=[
                    OpenApiExample(
                        'User Profile',
                        value={
                            'id': 1,
                            'full_name': 'John Doe',
                            'email': 'john.doe@example.com',
                            'is_active': True,
                            'created_at': '2024-12-01T10:00:00Z'
                        },
                        response_only=True,
                    )
                ]
            ),
            HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorSerializer,
                description="User does not have permission to view this profile",
                examples=[
                    OpenApiExample(
                        'Permission Denied',
                        value={
                            'error': 'You do not have permission to view this profile'
                        },
                        response_only=True,
                    )
                ]
            ),
            HTTP_404_NOT_FOUND: OpenApiResponse(
                description="User not found"
            ),
        },
    ),
    current_user=extend_schema(
        summary="Get Current User Profile",
        description="Retrieve the profile information of the currently authenticated user.",
        tags=['Users', 'Profile'],
        responses={
            HTTP_200_OK: OpenApiResponse(
                response=UserProfileSerializer,
                description="Current user profile retrieved successfully",
                examples=[
                    OpenApiExample(
                        'Current User Profile',
                        value={
                            'id': 1,
                            'full_name': 'John Doe',
                            'email': 'john.doe@example.com',
                            'is_active': True,
                            'created_at': '2024-12-01T10:00:00Z'
                        },
                        response_only=True,
                    )
                ]
            ),
        },
    ),
    update_profile=extend_schema(
        summary="Update User Profile",
        description="Update the profile information of the currently authenticated user. Supports both full (PUT) and partial (PATCH) updates.",
        tags=['Users', 'Profile'],
        request=UserUpdateProfileSerializer,
        responses={
            HTTP_201_CREATED: OpenApiResponse(
                description="Profile updated successfully",
                examples=[
                    OpenApiExample(
                        'Update Success',
                        value={
                            'message': 'Updated user profile',
                            'result': {
                                'id': 1,
                                'full_name': 'John Updated Doe',
                                'email': 'john.updated@example.com',
                                'is_active': True,
                                'created_at': '2024-12-01T10:00:00Z'
                            }
                        },
                        response_only=True,
                    )
                ]
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorSerializer,
                description="Validation error",
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        value={
                            'full_name': ['This field is required.'],
                            'email': ['Enter a valid email address.']
                        },
                        response_only=True,
                    )
                ]
            ),
        },
        examples=[
            OpenApiExample(
                'Update Full Name',
                value={
                    'full_name': 'John Updated Doe'
                },
                request_only=True,
            ),
            OpenApiExample(
                'Update Multiple Fields',
                value={
                    'full_name': 'John Updated Doe',
                    'email': 'john.updated@example.com'
                },
                request_only=True,
            )
        ]
    ),
    change_password=extend_schema(
        summary="Change Password",
        description="Change the password of the currently authenticated user. Returns new authentication tokens.",
        tags=['Users', 'Authentication'],
        request=ChangePasswordSerializer,
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Password changed successfully",
                examples=[
                    OpenApiExample(
                        'Password Change Success',
                        value={
                            'message': 'Password changed successfully',
                            'tokens': {
                                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                                'access': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
                            }
                        },
                        response_only=True,
                    )
                ]
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorSerializer,
                description="Validation error",
                examples=[
                    OpenApiExample(
                        'Invalid Current Password',
                        value={
                            'old_password': ['Current password is incorrect.']
                        },
                        response_only=True,
                    ),
                    OpenApiExample(
                        'Password Mismatch',
                        value={
                            'new_password': ['Password fields do not match.']
                        },
                        response_only=True,
                    )
                ]
            ),
        },
        examples=[
            OpenApiExample(
                'Change Password Request',
                value={
                    'old_password': 'current_password123',
                    'new_password': 'new_secure_password456',
                    'confirm_password': 'new_secure_password456'
                },
                request_only=True,
            )
        ]
    ),
    deactivate_user=extend_schema(
        summary="Deactivate Account",
        description="Deactivate the current user's account. Requires password confirmation. The account can be reactivated by administrators.",
        tags=['Users', 'Account Management'],
        request=OpenApiTypes.OBJECT,
        responses={
            HTTP_200_OK: OpenApiResponse(
                description="Account deactivated successfully",
                examples=[
                    OpenApiExample(
                        'Deactivation Success',
                        value={
                            'message': 'Account deactivated successfully'
                        },
                        response_only=True,
                    )
                ]
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorSerializer,
                description="Invalid request",
                examples=[
                    OpenApiExample(
                        'Missing Password',
                        value={
                            'error': 'Password is required to deactivate account'
                        },
                        response_only=True,
                    ),
                    OpenApiExample(
                        'Invalid Password',
                        value={
                            'error': 'Invalid password'
                        },
                        response_only=True,
                    )
                ]
            ),
        },
        examples=[
            OpenApiExample(
                'Deactivate Request',
                value={
                    'password': 'user_password123'
                },
                request_only=True,
            )
        ]
    ),
    delete_account=extend_schema(
        summary="Delete Account Permanently",
        description="Permanently delete the current user's account. This action is irreversible. Requires password and confirmation text 'DELETE'.",
        tags=['Users', 'Account Management'],
        request=OpenApiTypes.OBJECT,
        responses={
            HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Account deleted successfully",
                examples=[
                    OpenApiExample(
                        'Deletion Success',
                        value={
                            'message': 'Account john.doe@example.com deleted successfully'
                        },
                        response_only=True,
                    )
                ]
            ),
            HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorSerializer,
                description="Invalid request",
                examples=[
                    OpenApiExample(
                        'Missing Requirements',
                        value={
                            'error': 'Password and confirmation "DELETE" are required'
                        },
                        response_only=True,
                    ),
                    OpenApiExample(
                        'Invalid Password',
                        value={
                            'error': 'Invalid password'
                        },
                        response_only=True,
                    )
                ]
            ),
        },
        examples=[
            OpenApiExample(
                'Delete Account Request',
                value={
                    'password': 'user_password123',
                    'confirm': 'DELETE'
                },
                request_only=True,
            )
        ]
    ),
)
class UserViewSet(ViewSet):
    """User Profile ViewSet"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self,request):
        """List all users (only for staff)"""

        
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
        
    
    def retrieve(self,request,pk=None):
        
        """Retrieve user profile by ID"""
        
        
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
    
    
    @action(detail=False, methods=['put','patch'],url_path='me/update')
    def update_profile(self,request):
        """Update user profile"""
        
        
        serializer = UserUpdateProfileSerializer(
            request.user,
            data = request.data,
            partial = request.method == "PATCH"
        )
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'message':"Updated user profile",
                'result':UserProfileSerializer(request.user).data
            },status=status.HTTP_201_CREATED)
    
        
    @action(detail=False, methods=['post'], url_path='change_password')
    def change_password(self,request):
        """Change user password"""
        permissions_classes = IsOwnerOrReadOnly
        
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
        """Deactivate user account"""
        
        
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
        """Delete user account"""
        
        
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