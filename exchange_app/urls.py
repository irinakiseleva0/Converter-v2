from django.urls import path
from django.contrib.auth import views as auth_views
from .views import exchange, REG_FUNC, welcome

urlpatterns = [
    # стартовая страница
    path('', welcome, name='home'),

    # конвертер
    path('converter/', exchange, name='converter'),

    # регистрация
    path('register/', REG_FUNC, name='register'),

    # вход
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='exchange_app/login.html'
        ),
        name='login'
    ),

    # выход
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='home'   # после logout вернуть на welcome
        ),
        name='logout'
    ),
]
