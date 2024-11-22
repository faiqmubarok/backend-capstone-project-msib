from django.urls import path
from .views import userView
from .views import projectsView
from .views import transactionView

urlpatterns = [
    # User
    path('register/', userView.register, name='register'),
    path('login/', userView.login, name='login'),
    path('getUser/<str:userId>/', userView.getUser, name='getUser'),
    path('updateUser/<str:userId>/', userView.updateUser, name='updateUser'),

    # Project
    path('allProject/', projectsView.ProjectListView.as_view(), name='project-list'),
    path('project/<int:projectId>/', projectsView.ProjectDetailView.as_view(), name='project-detail'),

    # Transaction
    path('topup/', transactionView.TopUpView.as_view(), name='topup'),
]