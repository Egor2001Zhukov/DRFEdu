from rest_framework import serializers

from edu import models
from edu import validators
from edu.services import StripeService
from users.models import User


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
        fields = ['id', 'subscribe', 'title', 'description', 'lessons_count', 'lessons', 'price']


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = models.Payment
        fields = '__all__'


class PaymentOnlineSerializer(serializers.ModelSerializer):
    pay_url = serializers.SerializerMethodField()

    def get_pay_url(self, obj):
        return StripeService.create_billing_url(product_id=obj.course.id, name=obj.course.title,
                                                bayer_id=self.context['request'].user.id)

    class Meta:
        model = models.Payment
        fields = '__all__'
        extra_kwargs = {
            'course': {'required': True},
        }


class PaymentCashSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    course = CourseSerializer(read_only=True)
    amount = serializers.DecimalField(max_digits=9, decimal_places=2, required=True)

    class Meta:
        model = models.Payment
        fields = '__all__'
