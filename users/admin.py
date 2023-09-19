from django.contrib import admin

from users import models as m


# Register your models here.
@admin.register(m.User)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('email',)
