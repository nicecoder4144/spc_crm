from django.contrib import admin
from .models import Expenses, Payment, Area, Income, Worker_Payment

# Register your models here.

@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'branch', 'created_at')
    list_filter = ('branch', 'created_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('branch', 'group', 'student', 'created_at', 'month', 'amount')
    list_filter = ('branch', 'group', 'month', 'created_at')

@admin.register(Worker_Payment)
class Worker_PaymentAdmin(admin.ModelAdmin):
    list_display = ('worker', 'year', 'amount')
    list_filter = ('year', 'created_at')

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'area', 'amount', 'created_at')
    list_filter = ('branch', 'area', 'created_at')
