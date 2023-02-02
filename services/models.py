from django.db import models

# Create your models here.
from clientage.models import CustomerNames, PhoneNumbers
from siteservice.models import ModelPhone
from tgbot.models import Profile

STATUS_SERVICE = [
    ('ready', 'Готов'),
    ('without repair', 'Без ремонта'),
    ('during', 'В процессе')]


class AllServices(models.Model):
    user_id = models.ForeignKey(Profile, null=True, on_delete=models.DO_NOTHING, verbose_name="Телеграм ID", blank=True)
    imei_or_serial = models.CharField(max_length=100, verbose_name="Серия или IMEI", null=False)
    model = models.ForeignKey(ModelPhone, on_delete=models.CASCADE, verbose_name="Модель Техники", null=False)
    name_owner = models.ForeignKey(CustomerNames, on_delete=models.DO_NOTHING, verbose_name="Имя Клиента", null=True)
    phone_number = models.ForeignKey(PhoneNumbers, on_delete=models.DO_NOTHING, verbose_name="Номер телефона клиента",
                                     null=True)
    defect = models.CharField(max_length=150, verbose_name="Причина поломки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=70, choices=STATUS_SERVICE, default='during', blank=True)
    price = models.CharField(max_length=100, verbose_name='Стоимость', blank=True)
    income = models.CharField(max_length=100, verbose_name='Доход', blank=True)
    comment = models.TextField(max_length=150, verbose_name="Комментарии", blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
