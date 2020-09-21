# Generated by Django 3.1 on 2020-09-17 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('maximum_time', models.IntegerField(default=5)),
                ('inative', models.BooleanField(default=False)),
                ('status', models.CharField(default='Livre', max_length=9)),
                ('amount_of_loans', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('inative', models.BooleanField(default=False)),
                ('time_maximum', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan', models.DateTimeField(blank=True)),
                ('devolution', models.DateTimeField(blank=True, null=True)),
                ('amount_of_loans', models.IntegerField(default=0)),
                ('limit_time', models.DateTimeField(blank=True, null=True)),
                ('equipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='equipments.equipment')),
                ('user_devolution', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devolução', to='users.client')),
                ('user_loan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emprestimo', to='users.client')),
            ],
        ),
        migrations.AddField(
            model_name='equipment',
            name='type_equipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='equipments.equipment_type'),
        ),
    ]
