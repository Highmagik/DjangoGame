# Generated by Django 4.2.1 on 2023-05-20 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название игры')),
                ('description', models.TextField(max_length=500, verbose_name='Описание игры')),
                ('stage_number', models.IntegerField(default=1, verbose_name='Номер этапа')),
                ('end_date', models.DateField(verbose_name='Дата окончания этапа')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя пользователя')),
                ('stage1', models.BooleanField(default=False)),
                ('stage2', models.BooleanField(default=False)),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.game', verbose_name='Игра')),
            ],
        ),
    ]
