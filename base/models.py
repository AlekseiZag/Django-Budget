from django.db import models
from django.utils import timezone

from .inheritance import ProxySuper, ProxyManager
from django.contrib.auth.models import User


class Subcategory(models.Model):
    name = models.CharField('Подкатегория', max_length=255)

    def __str__(self):
        return self.name


class CategoryTypes(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name + str(self.pk)


class Color(models.Model):
    color = models.CharField(max_length=7, verbose_name='Цвет в 16-ти ричной системе', unique=True)

    def __str__(self):
        return f"{str(self.id)}|{self.color}"

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True, blank=True)
    name = models.CharField(verbose_name='Название категории', max_length=255)
    date_opened = models.DateField('Дата открытия категории', auto_now_add=True, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, verbose_name='Подкатегория', null=True,
                                    blank=True)
    type = models.ForeignKey(CategoryTypes, on_delete=models.PROTECT, verbose_name='Тип категории', null=True,
                             blank=True)

    color = models.ForeignKey(Color, on_delete=models.PROTECT, verbose_name='Цвет категории', null=True, blank=True)

    def __str__(self):
        return self.name + str(self.id)

    class Meta:
        unique_together = ('user', 'color', 'name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Operation(ProxySuper):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    datetime = models.DateTimeField('Дата операции', default=timezone.now)
    sum = models.DecimalField('Сумма операции', max_digits=10, decimal_places=2)
    comment = models.CharField('Комментарий к операции', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.proxy_name + ' ' + str(self.sum) + ' ' + str(self.user)

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def get_type(self, *args, **kwargs):
        return str(type(self))


class Income(Operation):
    class Meta:
        proxy = True

    objects = ProxyManager()


class Expense(Operation):
    class Meta:
        proxy = True

    objects = ProxyManager()


class Budget(models.Model):
    start_data = models.DateField('Начало срока')
    end_data = models.DateField('Конец срока')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Бюджет пользователя')


class BudgetDetails(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, verbose_name='Бюджет')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    sum = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
