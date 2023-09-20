from rest_framework import serializers

from edu import models as m


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Lesson
        fields = ['id', 'title', 'description', 'video', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = m.Course
        fields = ['id', 'title', 'description', 'lessons_count', 'lessons']


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = m.Payment
        fields = '__all__'
