from django.db import models

from users.models import User


# Create your models here.
class Course(models.Model):
    title = models.CharField(verbose_name='Название', max_length=150)
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='courses/')
    user = models.ForeignKey(User, verbose_name='Создатель', on_delete=models.CASCADE, related_name='courses',
                             blank=True, null=True)
    price = models.DecimalField(verbose_name='Сумма', max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(verbose_name='Название', max_length=150)
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='courses/')
    video = models.CharField(verbose_name='Ссылка на видео', max_length=150)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE, related_name='lessons')
    user = models.ForeignKey(User, verbose_name='Создатель', on_delete=models.CASCADE, related_name='lessons',
                             blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, related_name='payments',
                             blank=True, null=True)
    datetime = models.DateTimeField(verbose_name='Время и дата', auto_now_add=True)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.SET_NULL, related_name='payments',null=True)
    amount = models.DecimalField(verbose_name='Сумма', max_digits=9, decimal_places=2, blank=True, null=True)
    method = models.CharField(max_length=8, verbose_name='Способ',
                              choices=(('Наличные', 'Наличные'), ('Перевод', 'Перевод')), blank=True, null=True)

    def __str__(self):
        return f'{self.datetime}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscribe(models.Model):
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE, related_name='subscribes')
    user = models.ForeignKey(User, verbose_name='Создатель', on_delete=models.CASCADE, related_name='subscribes')
    is_active = models.BooleanField(default=False, verbose_name='Активна')

    def __str__(self):
        return f'Подписка пользователя {self.user} на курс {self.course}'

    class Meta:
        unique_together = ('course', 'user')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
