from django import forms
from .models import Expense, Income, Category
from .middleware import get_current_user


class SetForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ExpenseForm(SetForm, forms.ModelForm):
    category = forms.ModelChoiceField(queryset=None, label='Категория')

    class Meta:
        model = Expense
        fields = ('comment', 'category', 'sum')
        widgets = {
            'comment': forms.TextInput(attrs={'placeholder': 'Например: поход в кино'})
        }


class IncomeForm(SetForm, forms.ModelForm):
    category = forms.ModelChoiceField(queryset=None, label='Категория')

    class Meta:
        model = Income
        fields = ('comment', 'category', 'sum')
        widgets = {
            'comment': forms.TextInput(attrs={'placeholder': 'Например: зарплата за март'})
        }


class ExpCategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control width100"}),
        }


class IncCategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control width100"}),
        }
