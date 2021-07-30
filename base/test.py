# def check_for_ban(template, user_input):
#     words = user_input.replace(',', '').split()
#     print('words', words)
#     interset_result = list(set(words) & set(template))
#     print('interset_result', interset_result)
#     user_input = [word.replace(word, len(word) * '*') if word in interset_result else word for word in words]
#     return user_input
#
#
# print(check_for_ban(['suka', 'blayt'], 'suka, blayt, privet'))

from datetime import date, datetime

t_date = date(2020, 4, 23)
t_date = t_date.replace(day=11)
print(t_date)  # Выведет 2020-04-11
print(datetime.now())