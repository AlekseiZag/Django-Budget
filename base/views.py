from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView
from .models import Operation, Category, CategoryTypes, Expense, Color, Income
from .forms import ExpenseForm, IncomeForm, ExpCategoryAddForm, IncCategoryAddForm, ColorForm
from .service import Month, operations_per_month, sum_per_category, data_for_chart

import datetime

common_expense_list = ['Питание', 'Транспорт', 'Связь, интернет', 'Коммунальные платежи', 'Медицина',
                       'Страховки, налоги', 'Образование', 'Одежда', 'Кафе, рестораны', 'Спорт', 'Хобби, развлечения',
                       'Путешествия', 'Подарки', 'Прочее']


class CustomLoginView(LoginView):
    """Вход пользователя"""

    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('expense_list')


class RegisterPage(FormView):
    """Регистрация пользователя"""

    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            objs = [Category(name=item, user=user, type_id=1, color_id=common_expense_list.index(item) + 1) for item in
                    common_expense_list]
            objs.append(Category(name='Зарплата', user=user, type_id=2, color_id=len(common_expense_list) + 1))
            Category.objects.bulk_create(objs=objs)
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class CategoryDeleteView(DeleteView):
    """Удаление категории"""

    model = Category
    success_url = reverse_lazy('categories')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


@login_required
def expense_list(request):
    """
    Главная страница, отображение списка операций и добавление новых.
    Отображение статистики за месяц.
    """

    operations = Operation.objects.filter(user=request.user).order_by('-datetime')
    operation_paginator = Paginator(operations, 10)
    page_num = request.GET.get('page')
    page = operation_paginator.get_page(page_num)

    now = datetime.datetime.now()
    year = now.year
    month_number = now.month

    if request.method == 'POST':
        month_number = request.POST.get('month', None)
        year = int(request.POST.get('year', None))
        if int(month_number) == 0:
            year -= 1
            month_number = 12
        elif int(month_number) > 12:
            year += 1
            month_number = 1
    month_name = Month.get_name(int(month_number))

    expense_per_month = operations_per_month(Expense, year, month_number, request.user)
    expense_per_category = sum_per_category(Expense, year, month_number, request.user)

    income_per_month = operations_per_month(Income, year, month_number, request.user)
    income_per_category = sum_per_category(Income, year, month_number, request.user)

    data_exp, colors_exp = data_for_chart(expense_per_category)
    data_inc, colors_inc = data_for_chart(income_per_category)

    expense_form = ExpenseForm()
    income_form = IncomeForm()
    return render(request, 'base/index.html',
                  context={'operations': operations, 'expense_form': expense_form, 'income_form': income_form,
                           'expense_per_month': expense_per_month, 'income_per_month': income_per_month, 'year': year,
                           'month_name': month_name, 'month_number': month_number,
                           'expense_per_category': expense_per_category, 'income_per_category': income_per_category,
                           'data_exp': data_exp, 'colors_exp': colors_exp, 'colors_inc': colors_inc,
                           'data_inc': data_inc,
                           'count': operation_paginator.count, 'page': page})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def add_expense(request):
    """Добавление статьи расходов"""

    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            form = expense_form.save(commit=False)
            form.user = request.user
            form.save()
    return redirect('expense_list')


@login_required
def add_income(request):
    """Добавление статьи доходов"""

    if request.method == 'POST':
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            form = income_form.save(commit=False)
            form.user = request.user
            form.save()
    return redirect('expense_list')


@login_required
def add_color(request):
    """Добавление цвета для новой категории"""

    if request.method == 'POST':
        category_id = request.POST.get('category_id', None)
        try:
            current_category = Category.objects.get(pk=category_id)
            if current_category.user != request.user:
                messages.error(request, "Данная категория не Ваша!")
                return redirect('categories')
        except Category.DoesNotExist:
            messages.error(request, 'Данная катеория не найдена')
            return redirect('categories')
        except ValueError as e:
            messages.error(request, e)
            return redirect('categories')
        color_form = ColorForm(request.POST)
        color_obj, created = Color.objects.get_or_create(color=color_form.data['color'])
        current_category.color = color_obj
        try:
            current_category.save()
        except IntegrityError:
            messages.error(request, "Данный цвет уже ипользуется, выберите другой")
    return redirect('categories')


@login_required
def show_categories(request, action=None):
    """Отображение списка категорий и добавление новых"""

    categories_exp = Category.objects.filter(user=request.user, type__name='exp')
    categories_inc = Category.objects.filter(user=request.user, type__name='inc')
    context = {'categories_exp': categories_exp, 'categories_inc': categories_inc,
               'inc_form': IncCategoryAddForm, 'exp_form': ExpCategoryAddForm, 'form': ColorForm()}

    if request.method == 'POST':
        if action == 'add_inc':
            form = IncCategoryAddForm(request.POST)
            type_new_record = CategoryTypes.objects.filter(name='inc').first()
        elif action == 'add_exp':
            form = ExpCategoryAddForm(request.POST)
            type_new_record = CategoryTypes.objects.filter(name='exp').first()
        else:
            messages.error(request, "Произошла ошибка, попробуйте еще раз")
            return redirect('categories')
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.user = request.user
            new_record.type = type_new_record
            new_record.save()
        return redirect('categories')
    return render(request, 'base/categories.html', context)
