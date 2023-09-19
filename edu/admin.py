from django.contrib import admin

from edu import models as m


# Register your models here.
@admin.register(m.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(m.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)
