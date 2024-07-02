from django.test import TestCase
from notes.models import Note
from django.contrib.auth import get_user_model
from django.urls import reverse
from notes.forms import NoteForm

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

    def test_anonymous_client_has_no_form(self):
        url = reverse("notes:home")
        response = self.client.get(url)
        self.assertNotIn('form', response.context)

    def test_authorized_client_has_form(self):
        self.client.force_login(self.author)
        url = reverse("notes:add")
        response = self.client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
