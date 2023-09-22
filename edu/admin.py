from django.contrib import admin

from edu import models as m


# Register your models here.
@admin.register(m.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(m.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(m.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('datetime',)


@admin.register(m.Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
