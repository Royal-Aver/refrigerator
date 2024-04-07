from decimal import Decimal
from datetime import datetime, timedelta

DATE_FORMAT = '%Y-%m-%d'

def add(items, title, amount, expiration_date=None):
    """Добавляет в словарь продукты"""
    if title not in items:
        items[title] = []
    expiration_date = datetime.strptime(
        expiration_date,
        DATE_FORMAT
    ).date() if expiration_date else expiration_date

    items[title].append({'amount': amount, 'expiration_date': expiration_date})

def add_by_note(items, note):
    """Преобразует неформатные данные"""
    prod = note.split()
    try:
        if datetime.strptime(prod[-1], DATE_FORMAT):
            expiration_date = prod[-1]
            amount = prod[-2]
            title = ' '.join(prod[:-2])
            add(items, title, amount, expiration_date)
    except ValueError:
        amount = prod[-1]
        title = ' '.join(prod[:-1])
        add(items, title, amount)

def find(items, needle):
    """Поиск подстроки в словаре"""
    lst_find_prod = [product for product in items if needle.lower() in product.lower()]
    return lst_find_prod


def amount(items, needle):
    """Считает количество продукта"""
    products_lst = find(items, needle)
    sum = 0

    for product in products_lst:
        if product in items:
            for i in (items[product]):
                sum += Decimal(i['amount'])

    return sum


def expire(items, in_advance_days=0):
    """Выводит просроченный товар и его количество"""
    current_date = datetime.today().date()
    new_date = current_date + timedelta(days=in_advance_days)
    lst_prod = []

    for name, val in items.items():
        for k in val:
            if k['expiration_date'] and k['expiration_date'] <= new_date:
                res = name, k['amount']
                lst_prod.append(res)

            sum_dict = {}

            for key, value in lst_prod:
                if key in sum_dict:
                    sum_dict[key] += value
                else:
                    sum_dict[key] = value

            result = [(key, value) for key, value in sum_dict.items()]

    return result


goods = {
    'sausage': [
        {'amount': Decimal('0.3'),
         'expiration_date': datetime(2024, 4, 5).date()}
    ],
    'cake': [
        {'amount': Decimal('1.5'),
         'expiration_date': datetime(2024, 4, 6).date()}
    ]
}

add_product = add(goods,'sake', 1.9)
add_product = add(goods,'sake', 2.9,'2024-4-4')
note = add_by_note(goods, 'Eggs nut 1.5 2024-4-5')
note = add_by_note(goods, 'Eggs nut 1.6 2024-4-5')
note = add_by_note(goods, 'Egg hard 1.6')
# find = find(goods, 'eg')
amount = amount(goods, 'egg')
expire = expire(goods)

print(goods)
print(expire)

