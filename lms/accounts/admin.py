from django.contrib import admin

from accounts.models import CustomUser


@admin.action(description='Активировать выбранные элементы')
def activate_user(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='Деактивировать выбранные элементы')
def deactivate_user(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description='Сбросить аватары выбранных элементов')
def set_default_avatar(modeladmin, request, queryset):
    queryset.update(avatar='/path_to_default_avatar.jpg')


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'age', 'gender',
                    'phone', 'city',)
    list_display_links = 'id', 'email', 'first_name',
    list_filter = 'gender', 'city',
    search_fields = 'last_name', 'age', 'gender', 'phone', 'city',
    list_editable = 'last_name', 'age', 'gender', 'phone', 'city',

    actions = activate_user, deactivate_user, set_default_avatar
