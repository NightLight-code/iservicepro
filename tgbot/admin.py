from django.contrib import admin

# from tgbot.forms import ProfileForm
from tgbot.models import *
from tgbot.models import ProfileManager


# Register your models here.
def block_user(modeladmin, request, queryset):
    queryset.update(status='block')


block_user.short_description = "Заблокировать"


def not_block(modeladmin, request, queryset):
    queryset.update(status='not_block', )


not_block.short_description = "Разблокировать"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name', 'admin_or_not', 'block_user', 'notification')
    actions = [block_user, not_block, ]
    # form = ProfileForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')

    '''def get_queryset(self, request):
        return'''
