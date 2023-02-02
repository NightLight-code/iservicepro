from django.contrib import admin

# Register your models here.
from django.contrib.admin.views.main import ChangeList
#
from clientage.models import CustomerNames, PhoneNumbers
from services.models import AllServices
from siteservice.models import ModelPhone, NewPhone, \
    MacBook, Memory, AllColors, \
    Region, ModelMac
from tgbot.models import ProfileQueryset


def not_admin(modeladmin, request, queryset):
    queryset.update(admin_or_not='no_admin')


not_admin.short_description = "Не Админ"


def user_admin(modeladmin, request, queryset):
    queryset.update(admin_or_not='admin')


user_admin.short_description = "Админ"


def not_available(modeladmin, request, queryset):
    queryset.update(status='not_available')


not_available.short_description = "Нет в наличии"


def available(modeladmin, request, queryset):
    queryset.update(status='available', )


available.short_description = "В наличии"


def used(modeladmin, request, queryset):
    queryset.update(activ_or_not='Б/У')


used.short_description = "Б/У"


def new(modeladmin, request, queryset):
    queryset.update(activ_or_not='Новый')


new.short_description = "Новый"


def activ(modeladmin, request, queryset):
    queryset.update(activ_or_not='activ')


activ.short_description = "Активирован"


# Модель моделей айфон

# class ModelPhoneAdmin(admin.ModelAdmin):
#     # list_display = [field.name for field in Phone._meta.get_fields() if not field.many_to_many]
#     list_display = ['name_phone']
#     search_fields = ('name_phone',)


@admin.register(ModelPhone)
class PhoneModelAdmin(admin.ModelAdmin):
    list_display = ['name_phone']


# Модель новых айфон


@admin.register(NewPhone)
class NewPhoneAdmin(admin.ModelAdmin):
    list_display = ['model_phone',
                    'memory_phone',
                    'colors_phone',
                    'region_phone',
                    'price_phone',
                    'created_at',
                    'status',
                    'activ_or_not']

    search_fields = ['model_phone__name', 'memory_phone__memory', 'colors_phone__colors', 'price_phone']
    actions = [not_available, available, new, used, activ, ]


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ['memory']


@admin.register(AllColors)
class AllColorAdmin(admin.ModelAdmin):
    list_display = ['colors']


@admin.register(CustomerNames)
class CustomerNamesAdmin(admin.ModelAdmin):
    list_display = ['name_customer']


@admin.register(PhoneNumbers)
class PhoneNumbersAdmin(admin.ModelAdmin):
    list_display = ['user_phone_number']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['regions']


@admin.register(AllServices)
class AllServicesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'imei_or_serial', 'model', 'name_owner', 'phone_number', 'defect',
                    'created_at', 'update_at', 'status', 'price', 'comment']
    actions = [not_admin, user_admin]


@admin.register(MacBook)
class MacBookAdmin(admin.ModelAdmin):
    list_display = ['model_mac']
    actions = [not_available, available]


@admin.register(ModelMac)
class MacBookAdmin(admin.ModelAdmin):
    list_display = ['name_mac']
