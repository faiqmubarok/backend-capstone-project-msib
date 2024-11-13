from django.urls import path
from .views import userView

urlpatterns = [
    path('register/', userView.register, name='register'),
]