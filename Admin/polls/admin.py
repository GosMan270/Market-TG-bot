from django.contrib import admin
from .models import Mailing, Users
from django.core.mail import send_mass_mail
from django.conf import settings

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'address', 'phone', 'name', 'lastname', 'email')
    search_fields = ('name', 'lastname', 'email', 'phone')
    list_filter = ('role',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'created_at')
    actions = ['send_email']

    def send_email(self, request, queryset):
        # Собираем имейлы всех пользователей с заполненным email
        users = Users.objects.all()
        emails = [u.email for u in users if u.email]

        messages = []
        for mailing in queryset:
            for email in emails:
                messages.append((mailing.subject, mailing.body, settings.EMAIL_HOST_USER, [email]))

        send_mass_mail(messages, fail_silently=False)
        self.message_user(request, f"Письма отправлены на {len(emails)} адресов.")
    send_email.short_description = "Отправить выбранные рассылки по email"

