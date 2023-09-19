from django.urls import path
from rest_framework.routers import DefaultRouter

from edu import views as v
from edu.apps import EduConfig

app_name = EduConfig.name

router = DefaultRouter()
router.register(r'courses', v.CourseViewSet, basename='courses')

urlpatterns = [
                  path('lessons/', v.LessonListApiView.as_view(), name='lessons'),
                  path('lessons/<int:pk>', v.LessonAPIView.as_view(), name='lessons'),
                  path('payments/', v.PaymentListApiView.as_view(), name='payments')

              ] + router.urls
