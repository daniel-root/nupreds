# Generated by Django 3.0.4 on 2020-04-02 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0002_equipment_user_amount_of_loans'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipment_user',
            old_name='equiment',
            new_name='equipment',
        ),
        migrations.RenameField(
            model_name='equipment_user',
            old_name='usuario2',
            new_name='user_devolution',
        ),
        migrations.RenameField(
            model_name='equipment_user',
            old_name='usuario',
            new_name='user_loan',
        ),
    ]
