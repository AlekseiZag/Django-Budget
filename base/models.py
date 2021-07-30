from django.db import models
from .inheritance import ProxySuper, ProxyManager
from django.contrib.auth.models import User
from .middleware import get_current_user


class Subcategory(models.Model):
    name = models.CharField('Подкатегория', max_length=255)

    def __str__(self):
        return self.name


class CategoryTypes(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name + str(self.pk)


# class UserFilterCategory(models.Manager):
#     def get_queryset(self):
#         print(get_current_user())
#         return super().get_queryset().filter(user=get_current_user())


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    name = models.CharField(verbose_name='Название категории', max_length=255)
    date_opened = models.DateField('Дата открытия категории', auto_now_add=True, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, verbose_name='Подкатегория', null=True,
                                    blank=True)
    type = models.ForeignKey(CategoryTypes, on_delete=models.PROTECT, verbose_name='Тип категории', null=True,
                             blank=True)

    # objects = UserFilterCategory()

    def __str__(self):
        return self.name + f'({str(self.user)})'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Operation(ProxySuper):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    datetime = models.DateTimeField('Дата операции', auto_now_add=True)
    sum = models.DecimalField('Сумма операции', max_digits=10, decimal_places=2)
    comment = models.CharField('Комментарий к операции', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.proxy_name + ' ' + str(self.sum) + ' ' + str(self.user)

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def get_type(self, *args, **kwargs):
        return str(type(self))

    # def get_absolute_url(self):
    #     return reverse('company_detail', kwargs={'pk': self.pk})


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

# class Placement(models.Model):
#     party = models.ForeignKey(to=Operation, on_delete=models.CASCADE)
