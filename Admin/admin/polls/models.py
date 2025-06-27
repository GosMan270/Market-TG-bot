from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    role = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} {self.lastname}"

class Mailing(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    clients = models.ManyToManyField(Client)
    date_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title