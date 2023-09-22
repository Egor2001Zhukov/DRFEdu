from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from edu import models
from users.models import User


class LessonAPITestCase(APITestCase):
    """Напишите тесты, которые будут проверять корректность работы CRUD уроков и функционал работы подписки на обновления курса.
    Сохраните результат проверки покрытия тестами."""

    def setUp(self):
        self.user = User.objects.create_user(email='testemail@gmail.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.course = models.Course.objects.create(title='test_title', description='test_description',
                                                   preview='test.png')
        self.lesson = models.Lesson.objects.create(title='test_title', description='test_description',
                                                   preview='test.png', video='www.youtube.com/test', course=self.course,
                                                   user=self.user)

    def test_post(self):
        # Тестирование POST-запроса к API
        response = self.client.post(reverse('edu:lessons'),
                                    data={'title': 'test_title_2', 'description': 'test_description_2',
                                          'preview': 'test_2.png', 'video': 'www.youtube.com/test_2',
                                          'course': self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        # Тестирование GET-запроса к API
        response = self.client.get(reverse('edu:lessons'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self):
        # Тестирование GET-запроса к API
        response = self.client.get(reverse('edu:lessons', kwargs={'pk': self.lesson.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put(self):
        # Тестирование POST-запроса к API
        response = self.client.put(reverse('edu:lessons', kwargs={'pk': self.lesson.pk}),
                                   data={'title': 'test_title_put', 'description': 'test_description',
                                         'preview': 'test.png', 'video': 'www.youtube.com/test',
                                         'course': self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        # Тестирование POST-запроса к API
        response = self.client.delete(reverse('edu:lessons', kwargs={'pk': self.lesson.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscribeAPITestCase(APITestCase):
    """Напишите тесты, которые будут проверять корректность работы CRUD уроков и функционал работы подписки на обновления курса.
    Сохраните результат проверки покрытия тестами."""

    def setUp(self):
        self.user = User.objects.create_user(email='testemail@gmail.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.course = models.Course.objects.create(title='test_title', description='test_description',
                                                   preview='test.png')

    def test_post(self):
        # Тестирование POST-запроса к API
        response = self.client.post(reverse('edu:create_subscribe'),
                                    data={'course': self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete(self):
        # Тестирование POST-запроса к API
        subscribe = models.Subscribe.objects.create(course=self.course, user=self.user)
        response = self.client.delete(reverse('edu:delete_subscribe', kwargs={'pk': subscribe.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
