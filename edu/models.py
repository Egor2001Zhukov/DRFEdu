from django.db import models


# Create your models here.
class Course(models.Model):
    title = models.CharField(verbose_name='Название', max_length=150)
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='courses/')

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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
