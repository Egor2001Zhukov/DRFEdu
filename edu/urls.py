from django.urls import path
from rest_framework.routers import DefaultRouter

from edu import views as v
from edu.apps import EduConfig

app_name = EduConfig.name

urlpatterns = [
                  path('courses/', v.CourseListApiView.as_view(), name='courses'),
                  path('courses/<int:pk>', v.CourseAPIView.as_view(), name='courses'),
                  path('lessons/', v.LessonListApiView.as_view(), name='lessons'),
                  path('lessons/<int:pk>', v.LessonAPIView.as_view(), name='lessons'),
                  path('payments/', v.PaymentListApiView.as_view(), name='payments')

              ]
