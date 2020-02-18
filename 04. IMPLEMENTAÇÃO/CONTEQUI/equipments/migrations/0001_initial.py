# Generated by Django 3.0.1 on 2020-02-18 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(help_text='title of message.', max_length=10)),
                ('description', models.TextField()),
                ('typ', models.CharField(max_length=10)),
                ('maximum_time', models.IntegerField()),
            ],
        ),
    ]
