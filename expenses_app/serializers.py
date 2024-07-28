from rest_framework import serializers
from .models import User, Expenses, ExpenseShare

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile_number']

# Serializer for ExpenseShare model
class ExpenseShareSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()  # Add description field from the related expense

    class Meta:
        model = ExpenseShare
        fields = ['user', 'amount', 'percentage', 'description']

    def get_description(self, obj):
        # Get the description of the related expense
        return obj.expense.description
        
    def validate(self, data):
        # Validate the share based on the split method
        split_method = self.context['split_method']
        if split_method == 'exact' and 'amount' not in data:
            raise serializers.ValidationError({"amount": "This field is required for the exact split method."})
        elif split_method == 'percentage' and 'percentage' not in data:
            raise serializers.ValidationError({"percentage": "This field is required for the percentage split method."})
        elif split_method == 'equal' and ('amount' in data or 'percentage' in data):
            raise serializers.ValidationError("For equal split, only the user field is required.")
        return data

# Serializer for Expenses model
class ExpenseSerializer(serializers.ModelSerializer):
    shares = ExpenseShareSerializer(many=True)  # Include shares as a nested serializer

    class Meta:
        model = Expenses
        fields = ['id', 'description', 'total_amount', 'split_method', 'date', 'shares']
        
    def validate(self, data):
        # Validate the entire expense based on the split method
        split_method = data.get('split_method')
        shares = data.get('shares', [])
        
        if split_method == 'percentage':
            total_percentage = sum(share.get('percentage', 0) for share in shares)
            if total_percentage != 100:
                raise serializers.ValidationError("Total percentage must equal 100%.")
        elif split_method == 'exact':
            total_amount = sum(share.get('amount', 0) for share in shares)
            if total_amount != data.get('total_amount', 0):
                raise serializers.ValidationError("Total exact amounts must equal the total expense amount.")

        return data

    def create(self, validated_data):
        shares_data = validated_data.pop('shares')  # Remove shares data from validated data
        expense = Expenses.objects.create(**validated_data)  # Create the expense

        # Create shares based on the split method
        if expense.split_method == 'equal':
            equal_amount = expense.total_amount / len(shares_data)
            for share_data in shares_data:
                percentage = 100 / len(shares_data)
                ExpenseShare.objects.create(expense=expense, user=share_data['user'], amount=equal_amount, percentage=percentage)
        elif expense.split_method == 'exact':
            total_amount = expense.total_amount
            for share_data in shares_data:
                percentage = (share_data['amount'] / total_amount) * 100
                ExpenseShare.objects.create(expense=expense, **share_data, percentage=percentage)
        elif expense.split_method == 'percentage':
            for share_data in shares_data:
                amount = expense.total_amount * (share_data['percentage'] / 100)
                ExpenseShare.objects.create(expense=expense, user=share_data['user'], amount=amount, percentage=share_data['percentage'])

        return expense
    
    # Uncomment the following method if you need to customize the representation of the ExpenseSerializer
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['shares'] = ExpenseShareSerializer(instance.expenseshare_set.all(), many=True, context={'split_method': instance.split_method}).data
    #     return representation
