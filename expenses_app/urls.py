from django.urls import path
from .views import (
    UserCreateView, UserDetailView, ExpenseCreateView,
    UserExpensesView, OverallExpensesView, DownloadBalanceSheet
)

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='create-user'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('expenses/', ExpenseCreateView.as_view(), name='create-expense'),
    path('expenses/user/<int:user_id>/', UserExpensesView.as_view(), name='user-expenses'),
    path('expenses/overall/', OverallExpensesView.as_view(), name='overall-expenses'),
    path('users/download-balance-sheet/', DownloadBalanceSheet.as_view(), name='download-balance-sheet'),
]
