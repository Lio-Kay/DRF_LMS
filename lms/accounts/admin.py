from django.contrib import admin

from accounts.models import CustomUser


@admin.action(description='Деактивировать пользователя')
def deactivate_user(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'age', 'gender',
                    'phone', 'city',)
    list_display_links = 'id', 'email', 'first_name',
    list_filter = 'gender', 'city',
    search_fields = 'last_name', 'age', 'gender', 'phone', 'city',
    list_editable = 'last_name', 'age', 'gender', 'phone', 'city',

    actions = deactivate_user,
