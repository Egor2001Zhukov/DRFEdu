from django.urls import path
from rest_framework.routers import DefaultRouter

from edu import views
from edu.apps import EduConfig

app_name = EduConfig.name

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='courses')

urlpatterns = [
                  path('lessons/', views.LessonListApiView.as_view(), name='lessons'),
                  path('lessons/<int:pk>/', views.LessonAPIView.as_view(), name='lessons'),
                  path('payments/', views.PaymentListApiView.as_view(), name='payments')

              ] + router.urls
