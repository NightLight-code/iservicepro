from django.db import models


# Create your models here.


class CustomerNames(models.Model):
    """Имена всех пользователей сервиса"""
    name_customer = models.CharField(max_length=250, verbose_name="Имя клиента")

    def __str__(self):
        """
        Строка для представления имен всех пользователей
        """
        return self.name_customer

    class Meta:
        verbose_name = 'Имя клиента'
        verbose_name_plural = 'Имена клиентов'


class PhoneNumbers(models.Model):
    """Имена всех пользователей сервиса"""
    user_phone_number = models.CharField(max_length=150, verbose_name="Номер клиента")

    def __str__(self):
        """
        Строка для представления имен всех пользователей
        """
        return self.user_phone_number

    class Meta:
        verbose_name = 'Номер клиента'
        verbose_name_plural = 'Номера клиентов'

