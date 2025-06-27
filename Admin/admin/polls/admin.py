from django.contrib import admin
from .models import Client, Mailing

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'lastname', 'email', 'phone', 'role']
    search_fields = ['name', 'lastname', 'email', 'phone']

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_sent']
    filter_horizontal = ["clients"]