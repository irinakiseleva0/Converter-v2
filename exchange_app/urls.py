from django.urls import path
from .views import exchange, REG_FUNC

urlpatterns = [
    path('', exchange, name='home'),
    path('register/', REG_FUNC, name='register'),
]
