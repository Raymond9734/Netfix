from django.contrib import admin

from .models import User, Customer, Company


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for User model"""
    list_display = ("id", "username", "email")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin configuration for Company model"""
    list_display = ("user", "field_of_work", "rating", "description")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin configuration for Customer model"""
    list_display = ("user", "date_of_birth")
