from rest_framework import serializers

from .models import Branch, Room, Group
from finance.serializers import ExpensesAPISerializer, PaymentAPISerializer,\
    IncomeAPISerializer
from userapp.serializers import StudentPaymentAPISerializer

""" Admin panel uchun CRUD Serializers """
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Branch
        fields = ('__all__')

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('__all__')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields  =('__all__')

""" API """
class GroupAPISerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name')
    branch_slug = serializers.CharField(source='branch.slug')
    field_name = serializers.CharField(source='field.name')
    field_slug = serializers.CharField(source='field.slug')
    room_number = serializers.IntegerField(source='room.number')
    room_slug = serializers.CharField(source='room.slug')
    teacher_name = serializers.CharField(source='teacher.full_name')
    teacher_slug = serializers.CharField(source='teacher.slug')
    payments = PaymentAPISerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ('id',  'name', 'day', 'time',\
                  'branch', 'branch_name', 'branch_slug',\
                  'field', 'field_name', 'field_slug',\
                  'room', 'room_number', 'room_slug', 
                  'teacher', 'teacher_name', 'teacher_slug',
                  'payments',
                  )

class RoomAPISerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name')
    groups  = GroupAPISerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ('id', 'number', 'capacity', 'branch_name', 'groups')
    
class BranchAPISerializer(serializers.ModelSerializer):
    groups = GroupAPISerializer(many=True, read_only=True)
    rooms = RoomAPISerializer(many=True, read_only=True)
    expenses = ExpensesAPISerializer(many=True, read_only=True)
    incoms = IncomeAPISerializer(many=True, read_only=True)
    payments = PaymentAPISerializer(many=True, read_only=True)
    class Meta:
        model = Branch
        fields = ('id','name','slug','adress','groups','rooms',
                  'expenses','incoms','payments')
        
""" Studens payments """

class GroupAPIDetailSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name')
    branch_slug = serializers.CharField(source='branch.slug')
    field_name = serializers.CharField(source='field.name')
    field_slug = serializers.CharField(source='field.slug')
    field_cost = serializers.CharField(source='field.cost')
    room_number = serializers.IntegerField(source='room.number')
    room_slug = serializers.CharField(source='room.slug')
    teacher_name = serializers.CharField(source='teacher.full_name')
    teacher_slug = serializers.CharField(source='teacher.slug')

    # payments = PaymentAPISerializer(many=True, read_only=True)
    students = StudentPaymentAPISerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ('id',  'name', 'slug', 'day', 'time',\
                  'branch', 'branch_name', 'branch_slug',\
                  'field', 'field_name', 'field_slug', 'field_cost',\
                  'room', 'room_number', 'room_slug', 
                  'teacher', 'teacher_name', 'teacher_slug',
                  'students'
                  )


