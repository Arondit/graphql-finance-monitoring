from django.contrib import admin

from api.models import Category, Income, Profile, Waste

# Register your models here.

@admin.decorators.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Отображения профиля в панели администратора"""

@admin.decorators.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображения категории в панели администратора"""

@admin.decorators.register(Waste)
class WasteAdmin(admin.ModelAdmin):
    """Отображения расходов в панели администратора"""

@admin.decorators.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    """Отображения доходов в панели администратора"""
