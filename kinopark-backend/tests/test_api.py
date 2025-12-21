import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# Указываем pytest использовать базу данных
@pytest.mark.django_db
class TestCinemaFlow:
    
    def setup_method(self):
        self.client = APIClient()
        self.register_url = '/api/v1/auth/register/'
        self.login_url = '/api/v1/auth/login/'
        self.movies_url = '/api/v1/movies/'
        
        # Данные пользователя
        self.user_data = {
            "email": "test_pytest@kino.kz",
            "full_name": "Pytest User",
            "password": "StrongPassword123!",
            "password2": "StrongPassword123!"
        }

    def test_full_user_flow(self):
        """
        Тест полного цикла: Регистрация -> Логин -> Просмотр фильмов
        """
        # 1. Регистрация
        response = self.client.post(self.register_url, self.user_data)
        assert response.status_code == status.HTTP_201_CREATED
        print("\n✅ User Registered")

        # 2. Логин
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.login_url, login_data)
        assert response.status_code == 200
        assert 'access' in response.data['tokens']
        
        token = response.data['tokens']['access']
        print("✅ Login Successful, Token received")

        # 3. Получение списка фильмов (с токеном)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.movies_url)
        assert response.status_code == 200
        print("✅ Movies fetched successfully")