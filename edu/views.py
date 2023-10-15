from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from edu import models, tasks
from edu import serializators
from edu.permissions import IsModeratorOrCreator, IsModerator
from edu.services import StripeService


class CourseViewSet(ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializators.CourseSerializer
    permission_classes = [IsModeratorOrCreator, IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.save(user=self.request.user)
        StripeService.create_product(product_id=course.id, name=course.title, description=course.description)
        StripeService.create_price(price=int(course.price * 100), product_id=course.id, name=course.title)

    def perform_update(self, serializer):
        course = serializer.save()
        tasks.send_mainling.delay(course)


class LessonListCreateApiView(generics.ListCreateAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = serializators.LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save(user=self.request.user)
        tasks.send_mainling.delay(lesson.course)


class LessonAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = serializators.LessonSerializer
    permission_classes = [IsModeratorOrCreator, IsAuthenticated]


class PaymentListApiView(generics.ListAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializators.PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'method']
    ordering_fields = ['datetime']


class SubscribeCreateAPIView(generics.CreateAPIView):
    queryset = models.Subscribe.objects.all()
    serializer_class = serializators.SubscribeSerializer
    permission_classes = [IsModeratorOrCreator, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscribeDestroyAPIView(generics.DestroyAPIView):
    queryset = models.Subscribe.objects.all()
    serializer_class = serializators.SubscribeSerializer
    permission_classes = [IsModeratorOrCreator, IsAuthenticated]


class PaymentCashCreateAPIView(generics.CreateAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializators.PaymentCashSerializer
    permission_classes = [IsModerator, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(method='Наличные')


class PaymentOnlineCreateAPIView(generics.CreateAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializators.PaymentOnlineSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user, method='Перевод')
        payment.amount = int(payment.course.price * 100)
        payment.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        pay_url = serializer.data.get('pay_url')
        return Response({'payment': serializer.data, 'pay_url': pay_url}, status=status.HTTP_201_CREATED)
