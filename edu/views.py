from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics as g
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from edu import models as m
from edu import serializators as s


class CourseViewSet(viewsets.ModelViewSet):
    queryset = m.Course.objects.all()
    serializer_class = s.CourseSerializer


class LessonListApiView(g.ListCreateAPIView):
    queryset = m.Lesson.objects.all()
    serializer_class = s.LessonSerializer


class LessonAPIView(g.RetrieveUpdateDestroyAPIView):
    queryset = m.Lesson.objects.all()
    serializer_class = s.LessonSerializer


class PaymentListApiView(g.ListAPIView):
    queryset = m.Payment.objects.all()
    serializer_class = s.PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'method']
    ordering_fields = ['datetime']
