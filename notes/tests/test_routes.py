from django.test import Client, TestCase
from http import HTTPStatus
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model


User = get_user_model()


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testUser')
        cls.note = Note.objects.create(
            title='Заголовок новости',
            text='Тестовый текст',
            slug="myNote",
            author=User.objects.first()
        )

    def test_home_page(self):
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_note_page(self):
        url = reverse('notes:detail', kwargs={"slug": self.note.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
