from rest_framework import serializers
from django.test import TestCase
from ..models import User, Expenses, ExpenseShare
from ..serializers import UserSerializer, ExpenseSerializer, ExpenseShareSerializer
from rest_framework.test import APITestCase

class UserSerializerTest(TestCase):

    def test_valid_user_serializer(self):
        user_data = {
            'id': 1,
            'email': 'test@example.com',
            'name': 'Test User',
            'mobile_number': '1234567890'
        }
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_user_serializer(self):
        user_data = {
            'email': 'not-an-email',
            'name': '',
            'mobile_number': '123'
        }
        serializer = UserSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())

class ExpenseShareSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@example.com', name='Test User', mobile_number='1234567890')
        self.expense = Expenses.objects.create(description='Test Expense', total_amount=1000, split_method='exact', date='2023-01-01')

    def test_valid_expense_share_serializer(self):
        share_data = {
            'user': self.user.id,
            'amount': 500,
            'percentage': 50,
            'description': 'Test Description'
        }
        context = {'split_method': 'exact'}
        serializer = ExpenseShareSerializer(data=share_data, context=context)
        self.assertTrue(serializer.is_valid())

    def test_invalid_expense_share_serializer(self):
        share_data = {
            'user': self.user.id,
            'percentage': 50,
        }
        context = {'split_method': 'exact'}
        serializer = ExpenseShareSerializer(data=share_data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['amount']))

class ExpenseSerializerTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(name='user1', email='user1@example.com', mobile_number='1234567890')
        self.user2 = User.objects.create(name='user2', email='user2@example.com', mobile_number='1234567891')
        self.user3 = User.objects.create(name='user3', email='user3@example.com', mobile_number='1234567892')

    def create_serializer(self, data, context):
        return ExpenseSerializer(data=data, context=context)

    def test_valid_expense_serializer(self):
        data = {
            'description': 'Test Expense',
            'total_amount': 100,
            'split_method': 'equal',
            'date': '2024-07-27',
            'shares': [
                {'user': self.user1.id},
                {'user': self.user2.id}
            ]
        }
        context = {'split_method': 'equal'}
        serializer = self.create_serializer(data, context)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_expense_serializer(self):
        data = {
            'description': 'Test Expense',
            'total_amount': 100,
            'split_method': 'percentage',
            'date': '2024-07-27',
            'shares': [
                {'user': self.user1.id, 'percentage': 60},
                {'user': self.user2.id, 'percentage': 50}  # Total percentage != 100
            ]
        }
        context = {'split_method': 'percentage'}
        serializer = self.create_serializer(data, context)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'non_field_errors'})
