from django.db import models

class User(models.Model):
    email  = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    
    def __str__(self) :
        return self.name

class Expenses(models.Model):
    SPLIT_CHOICES = (
        ('equal', 'Equal'),
        ('percentage', 'Percentage'),
        ('exact', 'Exact'),
    )

    description = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits = 10, decimal_places=2)
    split_method = models.CharField(max_length=10, choices=SPLIT_CHOICES)
    date = models.DateField(auto_now_add= True)

class ExpenseShare(models.Model):
    expense = models.ForeignKey(Expenses, on_delete =models.CASCADE, db_index=True,related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index= True)
    amount = models.DecimalField(max_digits = 10, decimal_places=2, null=True, blank = True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank = True)

    def __str__(self) :
        return f"{self.user.name} owes {self.amount} for {self.expense.description}"