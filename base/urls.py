from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('categories/', views.show_categories, name='categories'),
    path('categories/<str:action>/', views.show_categories, name='categories'),
    path('category-delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='delete-category'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_income/', views.add_income, name='add_income'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('add_color/', views.add_color, name='add_color'),
]
