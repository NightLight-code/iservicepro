import re

from siteservice.models import ModelPhone, Memory, AllColors, Region, NewPhone


def write_data(data, filename='price.txt'):
    with open(filename, "w+") as f:
        f.write(f'{data}\n')
        f.close()
    create_price()


def create_price(count=3000):
    with open('../price.txt', 'r+') as s:
        file = s.readlines()
        for line in file:
            t = re.sub('[.,-]', ' ', line)
            phone_data = t.split()
            try:
                if len(phone_data) >= 7:
                    model = ' '.join(phone_data[:3])
                    memory = phone_data[3]
                    color = phone_data[4]
                    region = phone_data[5][-2:]
                    price = int(phone_data[6]) + count
                    add_data_in_db(model, memory, color, region, price)
                elif len(phone_data) == 6:
                    model = ' '.join(phone_data[:2])
                    memory = phone_data[2]
                    color = phone_data[3]
                    price = int(phone_data[5]) + count
                    region = phone_data[4][-2:]
                    add_data_in_db(model, memory, color, region, price)
                elif len(phone_data) == 5:
                    model = ' '.join(phone_data[:1])
                    memory = phone_data[1]
                    color = phone_data[2]
                    price = int(phone_data[4]) + count
                    region = phone_data[3][-2:]
                    add_data_in_db(model, memory, color, region, price)
            except ValueError as v:
                print(v)


def add_data_in_db(model, memory, color, region, price):
    try:
        p, _ = ModelPhone.objects.get_or_create(name=model)
        m, _ = Memory.objects.get_or_create(memory=memory)
        c, _ = AllColors.objects.get_or_create(colors=color)
        r, _ = Region.objects.get_or_create(regions=region)
        data = NewPhone.objects.filter(model_phone=p, memory_phone=m, colors_phone=c, region_phone=r).exists()
        if data:
            print(f"в наборе есть объекты {data}")
            data = NewPhone.objects.filter(model_phone=p, memory_phone=m, colors_phone=c, region_phone=r).update(
                price_phone=price)

        else:
            print(f'Нет данных {data}')
            new = NewPhone(model_phone=p, memory_phone=m, colors_phone=c, region_phone=r, price_phone=price)
            new.save()

    except ModelPhone.DoesNotExist as m:
        error_message = f'Произошла ошибка: {m}'
        print(error_message)
        raise m
