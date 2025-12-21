import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCinemaSystem:
    def setup_method(self):
        self.client = APIClient()
        self.register_url = '/api/v1/auth/register/'
        self.movies_url = '/api/v1/movies/'
        
    def test_end_to_end(self):
        """: Регистрация -> Получение токена -> Просмотр фильмов"""
        
        # 1. Регистрация
        user_data = {
            "email": "pytest_user@kino.kz",
            "full_name": "Tester",
            "password": "Password123!",
            "password2": "Password123!"
        }
        resp_reg = self.client.post(self.register_url, user_data)
        assert resp_reg.status_code == 201
        print("\n✅ User registered")

        # 2. Получение токена (он приходит сразу при регистрации в твоем коде)
        token = resp_reg.data['tokens']['access']
        assert token is not None
        print("✅ Token received")

        # 3. Доступ к фильмам (Нужен токен)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp_movies = self.client.get(self.movies_url)
        
        assert resp_movies.status_code == 200
        print(f"✅ Movies fetched: {len(resp_movies.data)}")