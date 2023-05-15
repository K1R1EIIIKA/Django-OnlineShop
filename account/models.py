from django.db import models


class UserInfo(models.Model):
    image = models.ImageField(upload_to='static/images/',
                              default='static/images/default.png')

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=100, default='')

    name = models.CharField(max_length=100, default='')
    surname = models.CharField(max_length=100, default='')
    patronymic = models.CharField(max_length=100, default='')

    class Meta:
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'

    def __str__(self):
        return self.user.username + ' - ' + self.surname + ' ' + self.name + ' ' + self.patronymic
