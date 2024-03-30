from django.shortcuts import render
from django.db.models import Sum, Count
from pprint import pprint
from datetime import date, datetime

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import Workers_Selery_StatSerializer, Input_and_output_Serializer, Quantity_Serializer
from userapp.models import Role, Worker, Student, Field
from mainapp.models import Branch, Group, Room
from finance.models import Expenses, Payment, Income, Worker_Payment, Area


# Create your views here.

""" WORKER STATISTICS """

class Workers_Selery_Stat_Viewset(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = Workers_Selery_StatSerializer
    permission_classes = [AllowAny,]

    def list(self, request, *args, **kwargs):
        workers = Worker.objects.filter(status=True) # barcha active ishchilar ro'yhati

        """ Bu oyni topib oldik / xxxx-xx-01 """
        today_y = date.today().year
        today_m = date.today().month
        today_x = date(today_y, today_m, 1)

        """ Ishchilarni roli  va puli uchun ro'yhat oldik """
        roles_and_money = {} # barcha davr uchun
        roles_and_money_monthly = {} # joriy oy uchun
        total_amount_all_time = {} # ishchilarning ummumiy maoshi 
        this_month_amount = {} # ishchilarning joriy oydagi maoshi

        roles = Role.objects.filter(status=True)
        for role in roles:
            roles_and_money[role.id] = 0
            roles_and_money_monthly[role.id] = 0

        for worker in workers:
            """ Ishchiga  qilingan barcha davr to'lovlarini topib oldik  """
            worker_payment_total_month = worker.worker_payments.all() # barcha davr to'lovlari
            total_amount_all_time[worker.id] = 0
            for key in total_amount_all_time:
                if worker.id == key:
                    for payment in worker_payment_total_month:
                        total_amount_all_time[key] += payment.amount # barcha davrda qilingan to'lov miqdorlarini qo'shib yig'ib oldik
            
            """ Ishchiga  qilingan joriy oydagi to'lovlarni topib oldik  """
            worker_payment_this_month = worker.worker_payments.filter(year=today_x) # joriy oy to'lovlarini filtirlab yig'ib oldik
            this_month_amount[worker.id] = 0
            for key in this_month_amount:
                if worker.id == key:
                    for payment in worker_payment_this_month:
                        this_month_amount[key] += payment.amount # joriy oyda qilingan to'lov miqdorlarini qo'shib yig'ib oldik

            """ Role va ulardagi ummumiy pullarni hisobladik """
            for key in roles_and_money.keys():
                if worker.role.id == key:
                    # ummumiy pullar
                    for key1, value1 in total_amount_all_time.items():
                        if key1 == worker.id:
                            roles_and_money[key] += value1 # ummumiy pul un

                    # joriy
                    for key2, value2 in this_month_amount.items():
                        if key2 == worker.id:
                            roles_and_money_monthly[key] += value2 # joriy oy un

        """ Olingan ma'lumotlarni API ga aylantiramiz """
        data = {
            'role_salery_all_time' : roles_and_money,
            'role_salery_this_month' : roles_and_money_monthly,
            'worker_salery_all_time' : total_amount_all_time,
            'worker_salery_this_month' : this_month_amount,
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data)


class Input_and_output_Viewset(viewsets.ViewSet):

    """ Kirim va chiqim uchun Viewset """
    def list(self, request, *args, **kwargs):

        # kerakli obyektlar
        students_payment = Payment.objects.filter(status=True)
        all_incomes = Income.objects.filter(status=True)
        branches = Branch.objects.filter(status=True)
        areas = Area.objects.filter(status=True)
        expenses = Expenses.objects.filter(status=True)

        """ Bu oyni topib oldik / xxxx-xx-01 """
        today_y = date.today().year
        today_m = date.today().month
        today_x = date(today_y, today_m, 1)

        # Filial daromadlari uchun o'zgaruvchilar
        branches_yearly_incomes = {}
        branches_last_yearly_incomes = {}
        branches_monthly_incomes = {}
        branches_last_monthly_incomes = {}
        for branch in branches:
            branches_yearly_incomes[branch.id] = 0
            branches_last_yearly_incomes[branch.id] = 0
            branches_monthly_incomes[branch.id] = 0
            branches_last_monthly_incomes[branch.id] = 0


        """"  🔴🔴🔴----------------- KIRIM ------------------🔴🔴🔴 """
        """ Payment uchun o'zgaruvchilar """
        yearly_payments_for_month = {
            'yan':0,
            'fev':0,
            'mar':0,
            'apr':0,
            'may':0,
            'iyn':0,
            'iyl':0,
            'avg':0,
            'sen':0,
            'okt':0,
            'noy':0,
            'dek':0,
        }
        total_students_payment = 0
        yearly_students_payment = 0
        monthly_students_payment = 0
        last_yearly_student_payment = 0
        last_monthly_student_payment = 0
        
        """ paymentlarni hisoblash """
        for payment in students_payment:
            # ummumiy summa
            total_students_payment += payment.amount
            
            # bu yilgi summa
            if payment.created_at.year == today_y:
                yearly_students_payment += payment.amount

                # Bu yilgi summaning oylar kesimidagi miqdori
                for key in yearly_payments_for_month.keys():
                    if payment.month == key:
                        yearly_payments_for_month[key] += payment.amount
    
                #bu oydagi summa
                if payment.created_at.month == today_m:
                    monthly_students_payment += payment.amount

            # o'tgan yilgi summa
            if payment.created_at.year == today_y-1:
                last_yearly_student_payment += payment.amount

            # o'tgan oydagi summa
            if payment.created_at.month == today_m-1 and today_m-1 > 0: # fev-dek oylari uchun o'tgan oyning pulini hisoblash
                if payment.created_at.year == today_y:
                    last_monthly_student_payment += payment.amount
            elif today_m-1 < 1: # Agar yanvarda turgan bo'lsak, o'tgan yilgi dekabrni hisoblash
                if payment.created_at.year == today_y-1 and payment.created_at.month == 12:
                    last_monthly_student_payment += payment.amount
        

        # income uchun o'zgaruvchilar
        total_incomes = 0
        yearly_incomes = 0
        yearly_incomes_for_month = {
            'yan':0,
            'fev':0,
            'mar':0,
            'apr':0,
            'may':0,
            'iyn':0,
            'iyl':0,
            'avg':0,
            'sen':0,
            'okt':0,
            'noy':0,
            'dek':0,
        }
        last_yearly_incomes = 0
        monthly_income = 0
        last_monthly_income = 0

        """ Income larni hisoblash """
        for income in all_incomes:
            # umummiy
            total_incomes += income.amount
            # bu yilgi
            for key in branches_yearly_incomes.keys():
                if income.created_at.year == today_y:
                    yearly_incomes += income.amount
                    # bu yilgi summa branch kesimida
                    if income.branch.id == key:
                        branches_yearly_incomes[key] += income.amount

                    # Bu yilgi summaning oylar kesimidagi miqdori
                    for key in yearly_incomes_for_month.keys():
                        if income.month == key:
                            yearly_incomes_for_month[key] += income.amount
                    # bu oygi 
                    if income.created_at.month == today_m:
                        monthly_income += income.amount

                    # bu yilgi summa branch kesimida
                    if income.branch.id == key:
                        branches_monthly_incomes[key] += income.amount

                # o'tgan yilgi
                if income.created_at.year == today_y-1:
                    last_yearly_incomes += income.amount

                # o'tgan yilgi summa branch kesimida
                if income.branch.id == key:
                    branches_last_yearly_incomes[key] += income.amount
                    
            
                # o'tgan oydagi summa
                if income.created_at.month == today_m-1 and today_m-1 > 0: # fev-dek oylari uchun o'tgan oyning pulini hisoblash
                    if income.created_at.year == today_y:
                        last_monthly_income += income.amount
                    # o'tgan oylik summa branch kesimida
                    if income.branch.id == key:
                        branches_last_monthly_incomes[key] += income.amount

                elif today_m-1 < 1: # Agar yanvarda turgan bo'lsak, o'tgan yilgi dekabrni hisoblash
                    if income.created_at.year == today_y-1 and income.created_at.month == 12:
                        last_monthly_income += income.amount

                    # o'tgan oylik summa branch kesimida
                    if income.branch.id == key:
                        branches_last_monthly_incomes[key] += income.amount
                

        """ Payment va Income dan kelgan ummumiy daromad """
        total_gross_profit = total_students_payment + total_incomes
        yearly_gross_profit = yearly_students_payment + yearly_incomes
        last_yearly_gross_profit = last_yearly_student_payment + last_yearly_incomes
        monthly_gross_profit =  monthly_students_payment + monthly_income
        last_monthly_gross_profit = last_monthly_student_payment + last_monthly_income

        """" 🔴🔴🔴----------- XARAJAT ---------- 🔴🔴🔴 """
        total_expenses = 0
        yearly_expenses = 0
        last_yearly_expenses = 0
        monthly_expenses = 0
        last_monthly_expenses = 0

        for expens in expenses:
            # ummumiy summa
            total_expenses += expens.amount
            # bu yilgi summa
            if expens.created_at.year == today_y:
                yearly_expenses += expens.amount
    
                #bu oydagi summa
                if expens.created_at.month == today_m:
                    monthly_expenses += expens.amount

            # o'tgan yilgi summa
            if expens.created_at.year == today_y-1:
                last_yearly_expenses += expens.amount

            # o'tgan oydagi summa
            if expens.created_at.month == today_m-1 and today_m-1 > 0: # fev-dek oylari uchun o'tgan oyning pulini hisoblash
                if expens.created_at.year == today_y:
                    last_monthly_expenses += expens.amount
            elif today_m-1 < 1: # Agar yanvarda turgan bo'lsak, o'tgan yilgi dekabrni hisoblash
                if expens.created_at.year == today_y-1 and expens.created_at.month == 12:
                    last_monthly_expenses += expens.amount

        """ ------------ Sof foyda ------------ """
        total_net_profit = total_gross_profit - total_expenses
        yearly_net_profit = yearly_gross_profit - yearly_expenses
        last_yearly_net_profit = last_yearly_gross_profit - last_yearly_expenses
        monthly_net_profit = monthly_gross_profit - monthly_expenses
        last_monthly_net_profit = last_monthly_gross_profit - last_monthly_expenses

        serializer_data = {
            # total_gross_profit
            'total_gross_profit' : total_gross_profit,
            'yearly_gross_profit' : yearly_gross_profit,
            'last_yearly_gross_profit' : last_yearly_gross_profit,
            'monthly_gross_profit' : monthly_gross_profit,
            'last_monthly_gross_profit' : last_monthly_gross_profit,
            # payments
            'total_students_payment' : total_students_payment,
            'yearly_students_payment' : yearly_students_payment,
            'monthly_students_payment' : monthly_students_payment,
            'last_monthly_student_payment' : last_monthly_student_payment,
            'last_yearly_student_payment' : last_yearly_student_payment,
            'yearly_payments_for_month' : yearly_payments_for_month,
            # incomes
            'total_incomes' : total_incomes,
            'yearly_incomes' : yearly_incomes,
            'last_yearly_incomes' : last_yearly_incomes,
            'monthly_income' : monthly_income,            
            'last_monthly_income' : last_monthly_income,
            'yearly_incomes_for_month' : yearly_incomes_for_month,
            # incomes branch kesimida
            'branches_yearly_incomes' : branches_yearly_incomes,
            'branches_last_yearly_incomes' : branches_last_yearly_incomes,
            'branches_monthly_incomes' : branches_monthly_incomes,
            'branches_last_monthly_incomes' : branches_last_monthly_incomes,
            # expenses-xarajat
            'total_expenses' : total_expenses,
            'yearly_expenses' : yearly_expenses,
            'last_yearly_expenses' : last_yearly_expenses,
            'monthly_expenses' : monthly_expenses,
            'last_monthly_expenses' : last_monthly_expenses,
            'total_net_profit' : total_net_profit,
            'yearly_net_profit' : yearly_net_profit,
            'last_yearly_net_profit' : last_yearly_net_profit,
            'monthly_net_profit' : monthly_net_profit,
            'last_monthly_net_profit' : last_monthly_net_profit,

        }
        serializer = Input_and_output_Serializer(serializer_data)

        return Response(serializer.data)
    

class Quantity_Viewset(viewsets.ViewSet):

    """ Turli xil yo'nalishlar bo'yicha raqamlar """
    def list(self, request, *args, **kwargs):
        # workers
        all_workers_count = Worker.objects.filter(status=True).count()
        groups_count_count = Group.objects.filter(status=True).count()
        all_students_count = Student.objects.filter(status=True).count()
        all_branches_count = Branch.objects.filter(status=True).count()
        all_rooms_count = Room.objects.filter(status=True).count()
        
        
        
        all_workers = Worker.objects.filter(status=True)
        roles = Role.objects.filter(status=True)
        workers_in_role = {}
        for role in roles:
            workers_count = Worker.objects.filter(status=True, role=role.id).count()
            workers_in_role[role.id] =  workers_count

        # students
        fields = Field.objects.filter(status=True)
        students_in_fields = {}
        for field in fields:
            students_count = Student.objects.filter(status=True, field=field.id).count()
            students_in_fields[field.id] = students_count
        
        groups = Group.objects.filter(status=True)
        teachers_students_count = {}
        for teacher in all_workers:
            teachers_students_count[teacher.id] = 0
            for group in groups:
                if group.teacher.id == teacher.id:
                    teachers_students_count[teacher.id] += group.students.count()

        data = {
            'all_workers_count' : all_workers_count,
            'workers_in_role' : workers_in_role,
            'groups_count_count' : groups_count_count,
            'all_students_count' : all_students_count,
            'teachers_students_count' : teachers_students_count,
            'all_rooms_count' : all_rooms_count,
        }
        serializer = Quantity_Serializer(data)
        return Response(serializer.data)
    




    