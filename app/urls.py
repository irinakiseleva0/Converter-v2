from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main converter page
    path('', include('exchange_app.urls')),

    # Optionally you can add separate views later:
    # path('currency-converter/', include('exchange_app.urls')),
    # path('about-us/', include('about_app.urls')),
]
