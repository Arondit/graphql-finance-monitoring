# Generated by Django 4.0.4 on 2022-05-21 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
                ('limit', models.DecimalField(decimal_places=2, default=None, max_digits=2, null=True, verbose_name='Ограничения на траты в категории')),
                ('date_created', models.DateField(auto_now=True, verbose_name='Дата создания категории')),
            ],
        ),
        migrations.CreateModel(
            name='Waste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='На что были потрачены деньги')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=2, verbose_name='Количество потраченных денег')),
                ('datetime_created', models.DateTimeField(auto_now=True, verbose_name='Время траты денег')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.category', verbose_name='Категория расходов')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill', models.DecimalField(decimal_places=2, default=0, max_digits=2, verbose_name='Счет пользователя в рублях')),
                ('name', models.CharField(max_length=100, verbose_name='Имя пользователя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь-владелец профиля')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.profile', verbose_name='Профиль, к которому привязана категория расходов'),
        ),
    ]
