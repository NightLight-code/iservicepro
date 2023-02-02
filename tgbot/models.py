from django.db import models

STATUS_BLOCK = [
    ('block', 'Заблокирован'),
    ('not_block', 'Разблокирован')]

CHOICES_ADMIN = [
    ('admin', 'Админ'),
    ('no_admin', 'Не Админ')
]


class ProfileQueryset(models.QuerySet):
    def profile_id(self):
        return self.values_list('external_id', 'name')
        # user_id = self.in_bulk()


class ProfileManager(models.Manager):
    def get_queryset(self):
        # return super().get_queryset().filter()
        # return ProfileQueryset(self.model).filter()
        return ProfileQueryset(self.model)

    def profile_id(self):
        return self.get_queryset().profile_id()


class Profile(models.Model):
    external_id = models.CharField(max_length=100, verbose_name='ID Пользователя')
    name = models.CharField(max_length=150, verbose_name='Имя пользователя')
    admin_or_not = models.CharField(max_length=15, choices=CHOICES_ADMIN, default='not_admin', blank=True,
                                    verbose_name='Админ')
    block_user = models.CharField(max_length=15, choices=STATUS_BLOCK, default='not_block', blank=True,
                                  verbose_name='Черный список')
    notification = models.BooleanField(default=False, verbose_name="Уведомление")

    objects = models.Manager()
    profile_info = ProfileManager()

    def __str__(self):
        return f'{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    profile = models.ForeignKey(to='tgbot.Profile', verbose_name='Профиль', on_delete=models.PROTECT)

    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(verbose_name='Время получение', auto_now_add=True)

    def __str__(self):
        return f'{self.pk} от {self.profile} {self.text} {self.created_at}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
