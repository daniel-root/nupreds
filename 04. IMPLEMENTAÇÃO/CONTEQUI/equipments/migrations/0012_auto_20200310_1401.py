# Generated by Django 2.1.5 on 2020-03-10 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0011_auto_20200310_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='usuario',
            field=models.CharField(max_length=255),
        ),
    ]
