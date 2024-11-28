from django.urls import path
from .views import userView
from .views import projectsView
from .views import transactionView
from .views import portfolioView

urlpatterns = [
    # User
    path('register/', userView.register, name='register'),
    path('login/', userView.login, name='login'),
    path('getUser/<str:userId>/', userView.getUser, name='getUser'),
    path('updateUser/<str:userId>/', userView.updateUser, name='updateUser'),

    # Project
    path('allProject/', projectsView.ProjectListView.as_view(), name='project-list'),
    path('upcoming/', projectsView.UpcomingProjectView.as_view(), name='upcoming-project'),
    path('topFunds/', projectsView.TopFundsProjectView.as_view(), name='top-funds-project'),
    path('topProfit/', projectsView.TopProfitProjectView.as_view(), name='top-profit-project'),
    path('project/<int:projectId>/', projectsView.ProjectDetailView.as_view(), name='project-detail'),

    # Transaction
    path('topup/', transactionView.TopUpView.as_view(), name='topup'),
    path('withdraw/', transactionView.WithdrawView.as_view(), name='withdraw'),
    path('getTransaction/<int:userId>/', transactionView.userTransactions, name='getTransaction'),

    # Portfolio
    path('investmentStats/<int:userId>/', portfolioView.InvestmentStatsView.as_view(), name='investmentStats'),
    path('getPortfolio/<int:userId>/', portfolioView.PortfolioView.as_view(), name='getPortfolio'),
]