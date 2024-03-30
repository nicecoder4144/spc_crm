from django.contrib import admin
from .models import Branch, Room, Group

# Register your models here.
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", 'id', "adress", "status", "created_at",)
    list_filter = ("status", "created_at")
    list_editable = ("status",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("number", 'id', 'slug', 'branch', "capacity", "status", "created_at")
    list_filter = ("branch", 'capacity', 'status', 'created_at')
    list_editable = ("status","capacity")

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'branch', 'field', 'teacher', 'day', 'time', 'status')
    list_filter  = ('branch', 'field', 'teacher', 'day','time', 'status', 'created_at')
    list_editable = ('status', 'day', 'time')

    
