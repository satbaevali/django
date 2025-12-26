import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.auths.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


# Fixture to provide an API client for testing
@pytest.fixture
def api_client():
    return APIClient()


# Fixture to create a normal test user
@pytest.fixture
def test_user(db):
    return CustomUser.objects.create_user(
        email="test@example.com",
        full_name="Test User",
        password="SecurePass123!"
    )


# Fixture to create an admin/superuser
@pytest.fixture
def admin_user(db):
    return CustomUser.objects.create_superuser(
        email="admin@example.com",
        full_name="Admin",
        password="AdminPass123!"
    )


# Fixture to provide an authenticated client with a normal user
@pytest.fixture
def auth_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.mark.django_db
class TestFullSystem:
    # --- URLS ---
    reg_url = reverse("auth-register")              # Registration endpoint
    login_url = reverse("auth-login")              # Login endpoint
    refresh_url = reverse("auth-refresh-token")    # Token refresh endpoint
    verify_url = reverse("auth-verify-token")      # Token verification endpoint
    list_url = reverse("users-list")               # List users endpoint
    me_url = reverse("users-current-user")         # Current authenticated user info
    update_url = reverse("users-update-profile")   # Update user profile endpoint
    pass_url = reverse("users-change-password")    # Change password endpoint
    delete_url = reverse("users-delete-account")   # Delete account endpoint

    # ==========================================
    # 1. AUTHENTICATION TESTS
    # ==========================================
    def test_reg_ok(self, api_client):
        """Test successful registration with valid data"""
        res = api_client.post(
            self.reg_url,
            {
                "email": "unique_success_user@m.com",
                "full_name": "Test User",
                "password": "SecurePassword123!",
                "password2": "SecurePassword123!",
            },
        )
        assert res.status_code == 201

    def test_reg_fail_mismatch(self, api_client):
        """Test registration fails if passwords do not match"""
        assert api_client.post(
            self.reg_url, {"password": "1", "password2": "2"}
        ).status_code == 400

    def test_reg_fail_exists(self, api_client, test_user):
        """Test registration fails if user with same email already exists"""
        assert api_client.post(self.reg_url, {"email": test_user.email}).status_code == 400

    def test_reg_fail_empty(self, api_client):
        """Test registration fails if no data provided"""
        assert api_client.post(self.reg_url, {}).status_code == 400

    def test_login_ok(self, api_client, test_user):
        """Test successful login with correct credentials"""
        assert api_client.post(
            self.login_url, {"email": test_user.email, "password": "SecurePass123!"}
        ).status_code == 200

    def test_login_fail_pass(self, api_client, test_user):
        """Test login fails with incorrect password"""
        assert api_client.post(
            self.login_url, {"email": test_user.email, "password": "Wrong"}
        ).status_code == 400

    def test_login_fail_no_user(self, api_client):
        """Test login fails if user does not exist"""
        assert api_client.post(
            self.login_url, {"email": "no@m.com", "password": "1"}
        ).status_code == 400

    def test_login_fail_invalid_email(self, api_client):
        """Test login fails if email format is invalid"""
        assert api_client.post(
            self.login_url, {"email": "bad", "password": "1"}
        ).status_code == 400

    def test_refresh_ok(self, api_client, test_user):
        """Test token refresh with valid refresh token"""
        refresh = str(RefreshToken.for_user(test_user))
        assert api_client.post(self.refresh_url, {"refresh": refresh}).status_code == 200

    def test_refresh_fail(self, api_client):
        """Test token refresh fails with invalid token"""
        assert api_client.post(self.refresh_url, {"refresh": "bad"}).status_code == 401

    def test_verify_ok(self, auth_client):
        """Test token verification succeeds for authenticated client"""
        assert auth_client.get(self.verify_url).status_code == 200

    def test_verify_fail(self, api_client):
        """Test token verification fails for unauthenticated client"""
        assert api_client.get(self.verify_url).status_code == 401

    # ==========================================
    # 2. USERS TESTS
    # ==========================================
    def test_list_admin_ok(self, api_client, admin_user):
        """Admin user can list all users"""
        api_client.force_authenticate(user=admin_user)
        assert api_client.get(self.list_url).status_code == 200

    def test_list_user_forbidden(self, auth_client):
        """Normal user cannot list all users"""
        assert auth_client.get(self.list_url).status_code == 403

    def test_list_unauth(self, api_client):
        """Unauthenticated client cannot list users"""
        assert api_client.get(self.list_url).status_code == 401

    def test_list_has_count(self, api_client, admin_user):
        """Admin user listing users returns a count field"""
        api_client.force_authenticate(user=admin_user)
        res = api_client.get(self.list_url)
        assert "count" in res.data

    def test_me_ok(self, auth_client):
        """Authenticated user can access their own info"""
        assert auth_client.get(self.me_url).status_code == 200

    def test_me_unauth(self, api_client):
        """Unauthenticated client cannot access /me endpoint"""
        assert api_client.get(self.me_url).status_code == 401

    def test_me_data_correct(self, auth_client, test_user):
        """Check if /me returns correct user data"""
        res = auth_client.get(self.me_url)
        assert res.data["email"] == test_user.email

    def test_me_patch_not_allowed(self, auth_client):
        """PATCH method on /me endpoint is not allowed"""
        assert auth_client.patch(self.me_url).status_code == 405

    def test_update_ok(self, auth_client):
        """Test successful profile update"""
        assert auth_client.patch(self.update_url, {"full_name": "New"}).status_code == 200

    def test_update_fail_unauth(self, api_client):
        """Unauthenticated client cannot update profile"""
        assert api_client.patch(self.update_url).status_code == 401

    def test_update_put_ok(self, auth_client):
        """Test successful full profile update using PUT"""
        assert auth_client.put(
            self.update_url, {"full_name": "John", "email": "j@m.com"}
        ).status_code == 200

    def test_pass_change_ok(self, auth_client, test_user):
        """Test successful password change"""
        payload = {
            "old_password": "SecurePass123!",
            "new_password": "NewSecurePass789!",
            "new_password2": "NewSecurePass789!"
        }
        assert auth_client.post(self.pass_url, payload).status_code == 200

    def test_pass_fail_wrong_old(self, auth_client):
        """Test password change fails if old password is incorrect"""
        assert auth_client.post(self.pass_url, {"old_password": "X"}).status_code == 400

    def test_pass_fail_mismatch(self, auth_client):
        """Test password change fails if new passwords do not match"""
        payload = {"old_password": "SecurePass123!", "new_password": "A", "new_password2": "B"}
        assert auth_client.post(self.pass_url, payload).status_code == 400

    def test_pass_fail_empty(self, auth_client):
        """Test password change fails if payload is empty"""
        assert auth_client.post(self.pass_url, {}).status_code == 400

    def test_delete_ok(self, auth_client, test_user):
        """Test successful account deletion"""
        res = auth_client.post(self.delete_url, {"password": "SecurePass123!", "confirm": "DELETE"})
        assert res.status_code == 204

    def test_delete_fail_no_confirm(self, auth_client):
        """Test account deletion fails if confirmation text is wrong"""
        assert auth_client.post(self.delete_url, {"password": "1", "confirm": "NO"}).status_code == 400

    def test_delete_fail_wrong_pass(self, auth_client):
        """Test account deletion fails if password is incorrect"""
        assert auth_client.post(self.delete_url, {"password": "W", "confirm": "DELETE"}).status_code == 400

    def test_delete_unauth(self, api_client):
        """Unauthenticated client cannot delete account"""
        assert api_client.post(self.delete_url).status_code == 401

    def test_retrieve_self_ok(self, auth_client, test_user):
        """User can retrieve their own details"""
        url = reverse("users-detail", args=[test_user.id])
        assert auth_client.get(url).status_code == 200

    def test_retrieve_other_fail(self, auth_client, admin_user):
        """Normal user cannot retrieve other user's details"""
        url = reverse("users-detail", args=[admin_user.id])
        assert auth_client.get(url).status_code == 403

    def test_retrieve_admin_any_ok(self, api_client, admin_user, test_user):
        """Admin can retrieve any user's details"""
        api_client.force_authenticate(user=admin_user)
        url = reverse("users-detail", args=[test_user.id])
        assert api_client.get(url).status_code == 200

    def test_retrieve_not_found(self, api_client, admin_user):
        """Retrieving a non-existent user returns 404"""
        api_client.force_authenticate(user=admin_user)
        url = reverse("users-detail", args=[9999])
        assert api_client.get(url).status_code == 404
