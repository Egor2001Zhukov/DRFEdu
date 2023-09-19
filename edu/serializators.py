from rest_framework import serializers

from edu import models as m


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Course
        fields = ['id', 'title', 'description', 'preview']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Lesson
        fields = ['id', 'title', 'description', 'video', 'preview']
