from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import User, Expenses, ExpenseShare

# Test case for creating a user
class UserCreateViewTest(APITestCase):

    def test_create_user(self):
        url = reverse('create-user')  # Adjust the URL name based on your URL patterns
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'mobile_number': '1234567890'
        }
        response = self.client.post(url, data, format='json')  # Make a POST request to create a user
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Check if the user creation is successful

    def test_create_user_invalid(self):
        url = reverse('create-user')  # Adjust the URL name based on your URL patterns
        data = {
            'email': 'invalid-email',
            'name': '',
            'mobile_number': '123'
        }
        response = self.client.post(url, data, format='json')  # Make a POST request with invalid data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Check if the request fails due to invalid data

# Test case for expense-related operations
class ExpenseAPITestCase(APITestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create(email='user1@example.com', name='User One', mobile_number='1234567890')
        self.user2 = User.objects.create(email='user2@example.com', name='User Two', mobile_number='1234567891')
        self.user3 = User.objects.create(email='user3@example.com', name='User Three', mobile_number='1234567892')
        
        # Create a test expense with equal split
        self.expense1 = Expenses.objects.create(description='Test Expense 1', total_amount=1000, split_method='equal', date='2023-01-01')
        ExpenseShare.objects.create(expense=self.expense1, user=self.user1, amount=500, percentage=50)
        ExpenseShare.objects.create(expense=self.expense1, user=self.user2, amount=500, percentage=50)

    def test_create_expense_equal_split(self):
        url = reverse('create-expense')  # Adjust the URL name based on your URL patterns
        data = {
            'description': 'Dinner',
            'total_amount': 3000,
            'split_method': 'equal',
            'shares': [
                {'user': self.user1.id},
                {'user': self.user2.id},
                {'user': self.user3.id}
            ]
        }
        self.client.force_authenticate(user=self.user1)  # Authenticate the request
        response = self.client.post(url, data, format='json')  # Make a POST request to create an expense
        print('Equal Split Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Check if the expense creation is successful

    def test_create_expense_percentage_split(self):
        url = reverse('create-expense')  # Adjust the URL name based on your URL patterns
        data = {
            'description': 'Party',
            'total_amount': 4000,
            'split_method': 'percentage',
            'shares': [
                {'user': self.user1.id, 'percentage': 50},
                {'user': self.user2.id, 'percentage': 25},
                {'user': self.user3.id, 'percentage': 25}
            ]
        }
        self.client.force_authenticate(user=self.user1)  # Authenticate the request
        response = self.client.post(url, data, format='json')  # Make a POST request to create an expense
        print('Percentage Split Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Check if the expense creation is successful

    def test_create_expense_exact_split(self):
        url = reverse('create-expense')  # Adjust the URL name based on your URL patterns
        data = {
            'description': 'Ride',
            'total_amount': 2000,
            'split_method': 'exact',
            'shares': [
                {'user': self.user1.id, 'amount': 1000},
                {'user': self.user2.id, 'amount': 700},
                {'user': self.user3.id, 'amount': 300}
            ]
        }
        self.client.force_authenticate(user=self.user1)  # Authenticate the request
        response = self.client.post(url, data, format='json')  # Make a POST request to create an expense
        print('Exact Split Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Check if the expense creation is successful

    def test_create_expense_invalid_percentage_split(self):
        url = reverse('create-expense')  # Adjust the URL name based on your URL patterns
        data = {
            'description': 'Invalid Percentage Split',
            'total_amount': 1000,
            'split_method': 'percentage',
            'date': '2023-01-01',
            'shares': [
                {'user': self.user1.id, 'percentage': 30},
                {'user': self.user2.id, 'percentage': 30},
            ]
        }
        self.client.force_authenticate(user=self.user1)  # Authenticate the request
        response = self.client.post(url, data, format='json')  # Make a POST request with invalid percentage split
        print('Invalid Percentage Split Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Check if the request fails due to invalid percentage split

    def test_user_detail_view(self):
        url = reverse('user-detail', args=[self.user1.id])  # Adjust the URL name based on your URL patterns
        self.client.force_authenticate(user=self.user1)  # Authenticate the request
        response = self.client.get(url)  # Make a GET request to fetch user details
        print('User Detail Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check if the request is successful
        self.assertEqual(response.data['email'], self.user1.email)  # Check if the fetched user data is correct

    def test_user_expenses_view(self):
        url = reverse('user-expenses', args=[self.user1.id])  # Adjust the URL name based on your URL patterns
        self.client.force_authenticate(user=self.user1)  # Authenticate the request
        response = self.client.get(url)  # Make a GET request to fetch user expenses
        print('User Expenses Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check if the request is successful
        self.assertTrue(len(response.data) > 0)  # Check if the response contains expenses data

    def test_overall_expenses_view(self):
        url = reverse('overall-expenses')  # Adjust the URL name based on your URL patterns
        self.client.force_authenticate(user=self.user1)  # Authenticate the request
        response = self.client.get(url)  # Make a GET request to fetch overall expenses
        print('Overall Expenses Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check if the request is successful
        self.assertTrue('total_expense' in response.data)  # Check if the response contains total expense data

    def test_download_balance_sheet(self):
        url = reverse('download-balance-sheet')  # Adjust the URL name based on your URL patterns
        self.client.force_authenticate(user=self.user1)  # Authenticate the request
        response = self.client.get(url)  # Make a GET request to download the balance sheet
        print('Download Balance Sheet Response data:', response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check if the request is successful
        self.assertTrue(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')  # Check if the response is an Excel file
