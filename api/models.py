from django.db import models


class Profile(models.Model):
    """Профиль пользователя"""

    user = models.OneToOneField('auth.User', verbose_name='Пользователь-владелец профиля', on_delete=models.CASCADE)
    bill = models.DecimalField('Счет пользователя в рублях', decimal_places=2, default=0, max_digits=20)
    name = models.CharField('Имя пользователя', max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория расходов, определяется пользователем"""

    name = models.CharField('Название категории', max_length=100)
    profile = models.ForeignKey(
        'api.Profile', 
        verbose_name='Профиль, к которому привязана категория расходов', 
        on_delete=models.CASCADE,
    )
    limit = models.DecimalField(
        'Ограничения на траты в категории', 
        null=True, 
        default=None, 
        decimal_places=2, 
        max_digits=20,
    )
    date_created = models.DateField('Дата создания категории', auto_now=True)

    def __str__(self):
        return self.name


class Waste(models.Model):
    """Трата"""

    name = models.CharField('На что были потрачены деньги', max_length=200)
    amount = models.DecimalField('Количество потраченных денег', decimal_places=2, max_digits=20)
    category = models.ForeignKey('api.Category', verbose_name='Категория расходов', on_delete=models.PROTECT)
    datetime_created = models.DateTimeField('Время траты денег', auto_now=True)

    def __str__(self):
        return self.name
