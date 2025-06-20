from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):
    """Тестирование курса."""

    def setUp(self):
        """Прописываем тестовые данные курса."""
        self.user = User.objects.create(
            email="admin@example.com"
        )
        self.course = Course.objects.create(
            name="Тестовый курс", description="Тестовое описание курса", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Тестовое описание урока",
            course=self.course,
            owner=self.user,
        )
        self.subscription = Subscription.objects.create(
            user=self.user, course=self.course
        )
        self.client.force_authenticate(
            user=self.user
        )

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)


class LessonTestCase(APITestCase):
    """Тестирование урока."""

    def setUp(self):
        """Прописываем тестовые данные урока."""
        self.user = User.objects.create(
            email="admin@example.com"
        )
        self.course = Course.objects.create(
            name="Тестовый курс", description="Тестовое описание курса", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Тестовое описание урока",
            video_link="https://youtube.com/test",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(
            user=self.user
        )

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {
            "title": "newtest",
            "description": "newdescription",
            "video_link": "https://youtube.com/test",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title="newtest").exists())

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"title": "update test"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "update test")

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_subscription(self):
        url = reverse("materials:subscribe")
        data = {"course_id": self.course.pk}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")

        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_link": self.lesson.video_link,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


    def test_subscribe_to_course_no_ex(self):
        Subscription.objects.all().delete()
        url = reverse('lms:subscribe')
        data = {'course_id': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_to_course_no_au(self):
        Subscription.objects.all().delete()
        self.client.force_authenticate(user='')
        url = reverse('lms:subscribe')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)