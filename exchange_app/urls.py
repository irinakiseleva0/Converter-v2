from django.urls import path
from .views import exchange,  REG_FUNC


urlpatterns = [
    path('exchange-app', exchange),
    path('', REG_FUNC),
    #path('about_us',)
]