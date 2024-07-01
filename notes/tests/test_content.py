from django.test import TestCase
from django.conf import settings
from notes.models import Note
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class TestContent(TestCase):
    HOME_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='testUser')
        Note.objects.bulk_create(Note(
            title='Заголовок новости',
            text='Тестовый текст',
            slug=f"myNote{index}",
            author=cls.author) for index in range(11)
        )

    def test_notes_count(self):
        self.client.force_login(self.author)
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        notes_count = object_list.count()
        self.assertEqual(notes_count, 11)
