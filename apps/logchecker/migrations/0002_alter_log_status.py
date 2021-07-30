# Generated by Django 3.2.4 on 2021-07-26 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logchecker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='status',
            field=models.CharField(blank=True, choices=[['Ok', 'Ok'], ['Undefined', 'Undefined'], ['Warning', 'Warning'], ['Error', 'Error']], max_length=100, null=True),
        ),
    ]