from django.db.models import Sum


class Month:
    @staticmethod
    def get_name(num):
        months = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
                  9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}
        return months[num]

    @staticmethod
    def soon(num):
        months = {1: 'В январе', 2: 'В феврале', 3: 'В марте', 4: 'В апреле', 5: 'В мае', 6: 'В июне', 7: 'В июле',
                  8: 'В августе', 9: 'В сентябре', 10: 'В октябре', 11: 'В ноябре', 12: 'В декабре'}
        return months[num]

    @staticmethod
    def num(gen):
        months = {'Январь': 1, 'Февраль': 2, 'Март': 3, 'Апрель': 4, 'Май': 5, 'Июнь': 6, 'Июль': 7, 'Август': 8,
                  'Сентябрь': 9, 'Октябрь': 10, 'Ноябрь': 11, 'Декабрь': 12}
        print(months[gen])


def operations_per_month(cls_name, year, month_number, user):
    if cls_name.__name__ == 'Expense':
        return cls_name.objects.filter(datetime__year=year, datetime__month=month_number,
                                       user=user).aggregate(total_expense=Sum('sum'))
    elif cls_name.__name__ == 'Income':
        return cls_name.objects.filter(datetime__year=year, datetime__month=month_number,
                                       user=user).aggregate(total_income=Sum('sum'))


def sum_per_category(cls_name, year, month_number, user):
    query_lst = list(cls_name.objects.values('category_id', 'category__name', 'category__color__color').filter(
        datetime__year=year,
        datetime__month=month_number,
        user=user).annotate(
        common_sum=Sum('sum')).order_by('-common_sum'))
    for category in query_lst:
        category['operations_per_category'] = cls_name.objects.filter(
            datetime__year=year,
            datetime__month=month_number,
            user=user,
            category_id=category['category_id']).order_by('-datetime')
    return query_lst


def data_for_chart(category):
    data = [str(cat['common_sum']) for cat in category]
    colors = [cat['category__color__color'] for cat in category]
    return data, colors
