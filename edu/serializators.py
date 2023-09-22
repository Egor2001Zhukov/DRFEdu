from rest_framework import serializers

from edu import models
from edu import validators


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscribe
        fields = ['course']


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.CharField(validators=[validators.VideoValidator()])

    class Meta:
        model = models.Lesson
        fields = ['id', 'title', 'description', 'video', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscribe = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_subscribe(self, obj):
        request = self.context.get('request')
        user = request.user
        subscription = models.Subscribe.objects.filter(user=user, course=obj).first()
        return subscription is not None

    class Meta:
        model = models.Course
        fields = ['id', 'subscribe', 'title', 'description', 'lessons_count', 'lessons']


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = models.Payment
        fields = '__all__'
