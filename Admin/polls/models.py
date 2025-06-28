from django.db import models

class Users(models.Model):
    id = models.BigIntegerField(primary_key=True)
    role = models.IntegerField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'

class Mailing(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Текст письма")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject