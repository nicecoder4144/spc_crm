from django.contrib import admin
from .models import Role, Worker, Student, Field

# Register your models here.

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ("name", 'id', "cost", "duration", "status", "created_at")
    list_filter = ("duration", "status", "created_at")
    list_editable = ("status",)

@admin.register(Role)
class Role(admin.ModelAdmin):
    list_display = ('name', 'id', 'status',)
    list_editable = ('status',)
    
@admin.register(Worker)
class Worker(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'role', 'status',)
    list_filter = ('status', 'role',)
    list_editable = ('status', 'role',)
    
@admin.register(Student)
class Student(admin.ModelAdmin):
    list_display = ('full_name', 'field', 'day', 'time', 'status',)
    list_filter = ('status', 'field', 'day', 'time',)
    list_editable = ('status',)



    