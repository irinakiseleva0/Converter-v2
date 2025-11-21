from django.urls import path
from .views import exchange, REG_FUNC, welcome

urlpatterns = [
    # 1) Стартовая страница (welcome)
    path('', welcome, name='home'),

    # 2) Страница с конвертером
    path('converter/', exchange, name='converter'),

    # 3) Регистрация (по желанию)
    path('register/', REG_FUNC, name='register'),
]
