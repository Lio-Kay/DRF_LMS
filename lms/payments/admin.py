from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    fields = (('user', 'paid_section'),
              ('payment_type', 'payment_method'),
              ('payments_left',), )
    list_display = ('id', 'user_link', 'section_link', 'payment_type',
                    'payment_method', 'payments_left', 'last_payment_date',)
    list_display_links = ('id', 'payment_type', 'payment_method',
                          'payments_left', 'last_payment_date',)
    list_filter = 'payment_type', 'payment_method',
    search_fields = 'user', 'section_link',
    readonly_fields = ('payment_type', 'payment_method', 'payments_left',
                       'last_payment_date')

    def user_link(self, obj):
        try:
            link = mark_safe('<a href="{}">{}</a>'.format(
                reverse('admin:accounts_customuser_change',
                        args=(obj.user.pk,)),
                f'Пользователь: {obj.user.first_name} {obj.user.last_name}.'))
        except AttributeError:
            link = ''
        return link

    user_link.short_description = 'Пользователь'

    def section_link(self, obj):
        try:
            link = mark_safe('<a href="{}">{}</a>'.format(
                reverse('admin:education_section_change',
                        args=(obj.paid_section.pk,)),
                f'Название: {obj.paid_section.name}. '
                f'Статус: {obj.paid_section.status.replace("OPEN", "Открытый").replace("CLOSED", "Закрытый").replace("ARCHIVED", "Архивированный")}'))
        except AttributeError:
            link = ''
        return link

    section_link.short_description = 'Раздел'
