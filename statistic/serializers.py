from rest_framework import serializers

from userapp.models import Field, Role, Worker, Student


class Workers_Selery_StatSerializer(serializers.ModelSerializer):
    role_salery_all_time = serializers.DictField()
    role_salery_this_month = serializers.DictField()
    worker_salery_all_time = serializers.DictField()
    worker_salery_this_month = serializers.DictField()

    class Meta:
        model = Worker
        fields = (
            'role_salery_all_time',
            'role_salery_this_month',
            'worker_salery_all_time', 
            'worker_salery_this_month',
            )

class Input_and_output_Serializer(serializers.Serializer):
    #total_gross_profit
    total_gross_profit = serializers.DecimalField(max_digits=30, decimal_places=2)
    yearly_gross_profit = serializers.DecimalField(max_digits=30, decimal_places=2)
    last_yearly_gross_profit = serializers.DecimalField(max_digits=30, decimal_places=2)
    monthly_gross_profit = serializers.DecimalField(max_digits=30, decimal_places=2)
    last_monthly_gross_profit = serializers.DecimalField(max_digits=30, decimal_places=2)
    # payment
    total_students_payment = serializers.DecimalField(max_digits=20, decimal_places=2)
    yearly_students_payment = serializers.IntegerField()
    monthly_students_payment = serializers.IntegerField()
    last_yearly_student_payment = serializers.IntegerField()
    last_monthly_student_payment = serializers.IntegerField()
    yearly_payments_for_month = serializers.DictField()
    # income
    total_incomes  = serializers.DecimalField(max_digits=20, decimal_places=2)
    yearly_incomes   = serializers.DecimalField(max_digits=20, decimal_places=2)             
    last_yearly_incomes = serializers.DecimalField(max_digits=20, decimal_places=2)
    monthly_income = serializers.DecimalField(max_digits=20, decimal_places=2)
    last_monthly_income = serializers.DecimalField(max_digits=20, decimal_places=2)
    yearly_incomes_for_month = serializers.DictField()
    # income-branch
    branches_yearly_incomes = serializers.DictField()
    branches_last_yearly_incomes = serializers.DictField()
    branches_monthly_incomes = serializers.DictField()
    branches_last_monthly_incomes = serializers.DictField()
    # expenses -xarajat
    total_expenses = serializers.DecimalField(max_digits=20, decimal_places=2)
    yearly_expenses = serializers.DecimalField(max_digits=20, decimal_places=2)
    last_yearly_expenses = serializers.DecimalField(max_digits=20, decimal_places=2)
    monthly_expenses = serializers.DecimalField(max_digits=20, decimal_places=2)
    last_monthly_expenses = serializers.DecimalField(max_digits=20, decimal_places=2)
    # net_profite - sof foyda
    total_net_profit = serializers.DecimalField(max_digits=30, decimal_places=2)
    yearly_net_profit = serializers.DecimalField(max_digits=30, decimal_places=2)
    last_yearly_net_profit = serializers.DecimalField(max_digits=30, decimal_places=2)
    monthly_net_profit = serializers.DecimalField(max_digits=30, decimal_places=2)
    last_monthly_net_profit = serializers.DecimalField(max_digits=30, decimal_places=2)

class Quantity_Serializer(serializers.Serializer):
    all_workers_count = serializers.IntegerField()
    workers_in_role = serializers.DictField()
    groups_count_count = serializers.IntegerField()
    all_students_count = serializers.IntegerField()
    teachers_students_count = serializers.DictField()
    all_rooms_count = serializers.IntegerField()


