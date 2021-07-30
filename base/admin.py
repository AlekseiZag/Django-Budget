from django.contrib import admin
from .models import Operation, Category, Subcategory, Budget, BudgetDetails, CategoryTypes

# Register your models here.
admin.site.register(Operation)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Budget)
admin.site.register(BudgetDetails)
admin.site.register(CategoryTypes)
