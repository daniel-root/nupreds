# Generated by Django 2.1.5 on 2020-02-19 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0003_auto_20200219_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment_user',
            name='devolution',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
