from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from edu import models
from edu import serializators
from edu.permissions import IsModeratorOrCreator


class CourseViewSet(ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializators.CourseSerializer
    permission_classes = [IsModeratorOrCreator, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonListCreateApiView(generics.ListCreateAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = serializators.LessonSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = serializators.LessonSerializer
    permission_classes = [IsModeratorOrCreator, IsAuthenticated]


class PaymentListApiView(generics.ListAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializators.PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'method']
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
