# Generated by Django 4.2.23 on 2025-06-27 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='summa',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='client',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='client',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='lastname',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='client',
            name='role',
            field=models.CharField(max_length=20),
        ),
    ]
