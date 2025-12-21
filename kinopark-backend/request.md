# ========================================
# AUTH ENDPOINTS
# ========================================

# 1. РЕГИСТРАЦИЯ
POST /api/v1/auth/register/
Content-Type: application/json

Request:
{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
}

Response 201:
{
    "message": "Registration was successful",
    "user": {
        "id": 1,
        "full_name": "John Doe",
        "email": "user@example.com",
        "is_active": true,
        "created_at": "2024-12-01T10:00:00Z"
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJh...",
        "access": "eyJ0eXAiOiJKV1QiLCJh..."
    }
}

---

# 2. ВХОД
POST /api/v1/auth/login/
Content-Type: application/json

Request:
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}

Response 200:
{
    "message": "Login was successful",
    "user": {...},
    "tokens": {
        "refresh": "...",
        "access": "..."
    }
}

---

# 3. ВЫХОД
POST /api/v1/auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

Request:
{
    "refresh": "refresh_token_here"
}

Response 200:
{
    "message": "Logout is successful"
}

---

# 4. ОБНОВЛЕНИЕ ТОКЕНА
POST /api/v1/auth/refresh/
Content-Type: application/json

Request:
{
    "refresh": "refresh_token_here"
}

Response 200:
{
    "access": "new_access_token",
    "message": "Token refreshed successfully"
}

---

# 5. ПРОВЕРКА ТОКЕНА
GET /api/v1/auth/verify/
Authorization: Bearer <access_token>

Response 200:
{
    "valid": true,
    "user": {...}
}

# ========================================
# USER ENDPOINTS
# ========================================

# 6. ТЕКУЩИЙ ПОЛЬЗОВАТЕЛЬ
GET /api/v1/users/me/
Authorization: Bearer <access_token>

Response 200:
{
    "id": 1,
    "full_name": "John Doe",
    "email": "user@example.com",
    "is_active": true,
    "created_at": "2024-12-01T10:00:00Z"
}

---

# 7. ОБНОВЛЕНИЕ ПРОФИЛЯ
PATCH /api/v1/users/me/update/
Authorization: Bearer <access_token>
Content-Type: application/json

Request:
{
    "full_name": "John Smith"
}

Response 200:
{
    "message": "Profile updated successfully",
    "user": {...}
}

---

# 8. СМЕНА ПАРОЛЯ
POST /api/v1/users/change-password/
Authorization: Bearer <access_token>
Content-Type: application/json

Request:
{
    "old_password": "SecurePass123!",
    "new_password": "NewPass456!",
    "new_password2": "NewPass456!"
}

Response 200:
{
    "message": "Password changed successfully",
    "tokens": {
        "refresh": "...",
        "access": "..."
    }
}

---

# 9. СПИСОК ПОЛЬЗОВАТЕЛЕЙ (только staff)
GET /api/v1/users/
Authorization: Bearer <access_token>

Response 200:
{
    "count": 10,
    "results": [...]
}

---

# 10. ПОЛУЧИТЬ ПОЛЬЗОВАТЕЛЯ
GET /api/v1/users/{id}/
Authorization: Bearer <access_token>

Response 200:
{
    "id": 1,
    "full_name": "John Doe",
    "email": "user@example.com",
    ...
}

---

# 11. ДЕАКТИВАЦИЯ АККАУНТА
POST /api/v1/users/deactivate/
Authorization: Bearer <access_token>
Content-Type: application/json

Request:
{
    "password": "SecurePass123!"
}

Response 200:
{
    "message": "Account deactivated successfully"
}

---

# 12. УДАЛЕНИЕ АККАУНТА
DELETE /api/v1/users/delete/
Authorization: Bearer <access_token>
Content-Type: application/json

Request:
{
    "password": "SecurePass123!",
    "confirm": "DELETE"
}

Response 204:
{
    "message": "Account user@example.com deleted successfully"
}

# ========================================
# JWT TOKEN ENDPOINTS (альтернативные)
# ========================================

# 13. ПОЛУЧИТЬ ТОКЕН
POST /api/v1/token/
Content-Type: application/json

Request:
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}

Response:
{
    "refresh": "...",
    "access": "..."
}

---

# 14. ОБНОВИТЬ ТОКЕН
POST /api/v1/token/refresh/
Content-Type: application/json

Request:
{
    "refresh": "refresh_token"
}

Response:
{
    "access": "new_access_token"
}

---

# 15. ПРОВЕРИТЬ ТОКЕН
POST /api/v1/token/verify/
Content-Type: application/json

Request:
{
    "token": "access_token"
}

Response:
{} (200 OK если валидный)



| Группа | Метод | URL Путь | Описание |
| :--- | :--- | :--- | :--- |
| **AUTH** | POST | /api/v1/auth/register/ | Регистрация нового пользователя |
| **AUTH** | POST | /api/v1/auth/login/ | Вход в систему (получение токенов) |
| **AUTH** | POST | /api/v1/auth/logout/ | Выход из системы (отзыв refresh-токена) |
| **AUTH** | POST | /api/v1/auth/refresh/ | Обновление access-токена с помощью refresh-токена |
| **AUTH** | GET | /api/v1/auth/verify/ | Проверка валидности access-токена |
| **USERS** | GET | /api/v1/users/ | Список пользователей (требует прав staff) |
| **USERS** | GET | /api/v1/users/{id}/ | Получение данных конкретного пользователя |
| **USERS** | GET | /api/v1/users/me/ | Получение данных текущего авторизованного пользователя |
| **USERS** | PATCH | /api/v1/users/me/update/ | Обновление профиля текущего пользователя |
| **USERS** | POST | /api/v1/users/change-password/ | Смена пароля текущего пользователя |
| **USERS** | POST | /api/v1/users/deactivate/ | Деактивация аккаунта текущего пользователя |
| **USERS** | DELETE | /api/v1/users/delete/ | Удаление аккаунта текущего пользователя |
| **JWT** | POST | /api/v1/token/ | Получить токен (альтернативный вход) |
| **JWT** | POST | /api/v1/token/refresh/ | Обновить токен (альтернативный) |
| **JWT** | POST | /api/v1/token/verify/ | Проверить токен (альтернативный) |