from django.contrib import admin

from . forms import ColorForm
from .models import Operation, Category, Subcategory, Budget, BudgetDetails, CategoryTypes, Color


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    # list_display = ('id', 'name', 'color',)


class ColorAdmin(admin.ModelAdmin):
    form = ColorForm



admin.site.register(Operation)
admin.site.register(Color, ColorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory)
admin.site.register(Budget)
admin.site.register(BudgetDetails)
admin.site.register(CategoryTypes)
