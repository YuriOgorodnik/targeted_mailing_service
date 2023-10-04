from django.contrib import admin

from mailings.models import Client, MailingList, MailingMessage, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email',)


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'frequency', 'status',)


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('last_attempt_datetime', 'status',)
