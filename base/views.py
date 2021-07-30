from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView

from .models import Operation, Category, CategoryTypes
from .forms import ExpenseForm, IncomeForm, ExpCategoryAddForm, IncCategoryAddForm

common_expense_list = ['Питание', 'Транспорт', 'Связь, интернет', 'Коммунальные платежи', 'Медицина',
                       'Страховки, налоги',
                       'Образование', 'Одежда', 'Кафе, рестораны', 'Спорт', 'Хобби, развлечения', 'Путешествия',
                       'Подарки',
                       'Прочее']


# common_income_list = ['Зарплата', ]


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('expense_list')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            objs = [Category(name=item, user=user, type_id=1) for item in common_expense_list]
            objs.append(Category(name='Зарплата', user=user, type_id=2))
            Category.objects.bulk_create(objs=objs)
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


@login_required
def expense_list(request):
    operations = Operation.objects.filter(user=request.user)
    expense_form = ExpenseForm()
    expense_form.fields['category'].queryset = Category.objects.filter(type__name='exp', user=request.user)
    income_form = IncomeForm()
    income_form.fields['category'].queryset = Category.objects.filter(type__name='inc', user=request.user)
    return render(request, 'base/index.html',
                  context={'operations': operations, 'expense_form': expense_form, 'income_form': income_form})


def logout_view(request):
    logout(request)
    return redirect('/')


def add_expense(request):
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            form = expense_form.save(commit=False)
            form.user = request.user
            form.save()
    return redirect('expense_list')


def add_income(request):
    if request.method == 'POST':
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            form = income_form.save(commit=False)
            form.user = request.user
            form.save()
    return redirect('expense_list')


@login_required
def show_categories(request, action=None):
    objs = [Category(name=item, user=request.user, type_id=1) for item in common_expense_list]
    objs.append(Category(name='Зарплата', user=request.user, type_id=2))
    categories_exp = Category.objects.filter(user=request.user, type__name='exp')
    categories_inc = Category.objects.filter(user=request.user, type__name='inc')
    context = {'categories_exp': categories_exp, 'categories_inc': categories_inc,
               'inc_form': IncCategoryAddForm, 'exp_form': ExpCategoryAddForm}

    if request.method == 'POST':
        if action == 'add_inc':
            form = IncCategoryAddForm(request.POST)
            type_new_record = CategoryTypes.objects.filter(name='inc').first()
        elif action == 'add_exp':
            form = ExpCategoryAddForm(request.POST)
            type_new_record = CategoryTypes.objects.filter(name='exp').first()
        else:
            form = None
            type_new_record = None
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.user = request.user
            new_record.type = type_new_record
            new_record.save()
        return redirect('categories')
    return render(request, 'base/categories.html', context)
