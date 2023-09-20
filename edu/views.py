from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics as g
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from edu import models as m
from edu import serializators as s


class IsModeratorOrCreator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ['GET', 'POST']:
                return True
            elif request.user == view.get_object().user:
                return True
            else:
                if request.user.groups.filter(name="moderators").exists():
                    if request.method == 'PUT':
                        print('Я модератор')
                        return True
        return False


class CourseListApiView(g.ListCreateAPIView):
    queryset = m.Course.objects.all()
    serializer_class = s.CourseSerializer

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.user = self.request.user
        new_course.save()


class CourseAPIView(g.RetrieveUpdateDestroyAPIView):
    queryset = m.Course.objects.all()
    serializer_class = s.CourseSerializer
    permission_classes = [IsModeratorOrCreator]


class LessonListApiView(g.ListCreateAPIView):
    queryset = m.Lesson.objects.all()
    serializer_class = s.LessonSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class LessonAPIView(g.RetrieveUpdateDestroyAPIView):
    queryset = m.Lesson.objects.all()
    serializer_class = s.LessonSerializer
    permission_classes = [IsModeratorOrCreator]


class PaymentListApiView(g.ListAPIView):
    queryset = m.Payment.objects.all()
    serializer_class = s.PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'method']
    ordering_fields = ['datetime']
