# Generated by Django 4.1.3 on 2022-12-16 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='birth_date',
            field=models.DateField(verbose_name='生日'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hire_date',
            field=models.DateField(verbose_name='入职时间'),
        ),
    ]