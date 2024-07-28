from django.shortcuts import render

from rest_framework import generics, status, permissions
from .models import User, Expenses, ExpenseShare
from .serializers import UserSerializer, ExpenseSerializer, ExpenseShareSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
import csv

# User creation view
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Serialize and validate input data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Save the user object if valid
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User detail view
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            # Retrieve user details
            return super().retrieve(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response({"errors": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User expenses view
class UserExpensesView(APIView):

    def get(self, request, user_id):
        try:
            # Retrieve expenses for a specific user
            user = User.objects.get(id=user_id)
            expenses = ExpenseShare.objects.filter(user=user)
            serializer = ExpenseShareSerializer(expenses, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"errors": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Expense creation view
class ExpenseCreateView(generics.CreateAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Get the split method and validate input data
            split_method = request.data.get('split_method')
            serializer = self.get_serializer(data=request.data, context={'split_method': split_method})
            serializer.is_valid(raise_exception=True)
            # Save the expense object if valid
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to get all expenses
class OverallExpensesView(APIView):
    
    def get(self, request):
        try:
            # Retrieve and serialize all expenses
            expenses = Expenses.objects.all()
            serializer = ExpenseSerializer(expenses, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to download the balance sheet as a CSV file
class DownloadBalanceSheet(APIView):

    def get(self, request):
        try:
            users = User.objects.all()
            all_expenses = Expenses.objects.all()
            
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'
            
            writer = csv.writer(response)
            # Write individual expenses
            writer.writerow(['Individual Expenses'])
            writer.writerow([])
            writer.writerow(['User', 'Description', 'Total_Amount', 'Split_Method', 'Date', 'Share_Amount', 'Share_Percentage'])
            
            for user in users:
                user_expenses = Expenses.objects.filter(shares__user=user).distinct()
                for expense in user_expenses:
                    for share in expense.shares.filter(user=user):
                        writer.writerow([
                            user.name,
                            expense.description, 
                            expense.total_amount, 
                            expense.split_method,
                            expense.date, 
                            share.amount,
                            share.percentage
                        ])
                writer.writerow([]) 
                
            # Write overall expenses
            writer.writerow([])
            writer.writerow(['Overall Expenses'])
            writer.writerow(['Description', 'Total_Amount', 'Split_Method', 'Date'])
            
            for expense in all_expenses:
                writer.writerow([
                    expense.description, 
                    expense.total_amount, 
                    expense.split_method, 
                    expense.date
                ])
            
            return response
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
