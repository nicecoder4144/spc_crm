from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Expenses, Payment, Area, Income, Worker_Payment

""" CRUD API """
class ExpensesSerializer(ModelSerializer):
    class Meta:
        model = Expenses
        fields = ('__all__')

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ('__all__')

class AreaSerializer(ModelSerializer):
    class Meta:
        model = Area
        fields = ('__all__')

class IncomeSerializer(ModelSerializer):
    class Meta:
        model = Income
        fields = ('__all__')

class Worker_PaymentSerializer(ModelSerializer):
    class Meta:
        model = Worker_Payment
        fields =('__all__')

""" API """
class ExpensesAPISerializer(ModelSerializer):
    branch_name = serializers.CharField(source='branch.name')
    branch_slug = serializers.CharField(source='branch.slug')
    class Meta:
        model = Expenses
        fields = ('id', 'name', 'slug', 'amount', 'comment',\
                  'branch', 'branch_name', 'branch_slug')

class PaymentAPISerializer(ModelSerializer):
    branch_name = serializers.CharField(source='branch.name')
    branch_slug = serializers.CharField(source='branch.slug')
    group_name = serializers.CharField(source='group.name')
    group_slug = serializers.CharField(source='group.slug')
    student_name = serializers.CharField(source='student.full_name')
    student_slug = serializers.CharField(source='student.slug')
    class Meta:
        model = Payment
        fields = (
            'id', 
            'month', 'amount', 
                  'branch', 'branch_name', 'branch_slug',
                  'group', 'group_name', 'group_slug',
                  'student', 'student_name', 'student_slug',
                  )

class IncomeAPISerializer(ModelSerializer):
    branch_name = serializers.CharField(source='branch.name')
    branch_slug = serializers.CharField(source='branch.slug')
    area_name = serializers.CharField(source='area.name')
    area_slug = serializers.CharField(source='area.slug')
    class Meta:
        model = Income
        fields = ('id', 'name', 'amount', 'comment', 
                    'branch', 'branch_name', 'branch_slug',
                    'area', 'area_name', 'area_slug',
                    )

class AreaAPISerializer(ModelSerializer):
    incoms = IncomeAPISerializer(many=True, read_only=True)
    class Meta:
        model = Area
        fields = ('id', 'name', 'slug', 'incoms')

""" For Student paymens info """
class PaymentStudentAPISerializer(ModelSerializer):
    branch_name = serializers.CharField(source='branch.name')
    branch_slug = serializers.CharField(source='branch.slug')
    group_name = serializers.CharField(source='group.name')
    group_slug = serializers.CharField(source='group.slug')
    student_name = serializers.CharField(source='student.full_name')
    student_slug = serializers.CharField(source='student.slug')
    class Meta:
        model = Payment
        fields = (
            'id', 
            'month', 'amount', 
                  'branch', 'branch_name', 'branch_slug',
                  'group', 'group_name', 'group_slug',
                  'student', 'student_name', 'student_slug',
                  )




