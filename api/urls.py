from django.urls import path
from .views import userView

urlpatterns = [
    path('register/', userView.register, name='register'),
    path('login/', userView.login, name='login'),
    path('getUser/<str:userId>/', userView.getUser, name='getUser'),
    path('updateUser/<str:userId>/', userView.updateUser, name='updateUser'),
]