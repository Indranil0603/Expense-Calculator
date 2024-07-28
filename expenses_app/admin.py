from django.contrib import admin
from .models import Expenses, ExpenseShare, User

@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'total_amount', 'split_method', 'date')

@admin.register(ExpenseShare)
class ExpenseShareAdmin(admin.ModelAdmin):
    list_display = ('id', 'expense', 'user', 'amount', 'percentage')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'mobile_number')
