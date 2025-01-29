from django.urls import path
from . import views  # Импортируем views из вашего приложения

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_image/', views.add_image, name='add_image'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
]