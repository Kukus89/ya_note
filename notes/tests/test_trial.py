from django.test import TestCase
from notes.models import Note
# from django.conf import settings
from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404

user = get_user_model()


class TestNote(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.note = Note.objects.create(
            title='Заголовок новости',
            text='Тестовый текст',
            slug="моя закладочка",
            author_id=user.objects.create(
                username='testuser',
            )
        )

    def test_successful_creation(self):
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)

    def test_title(self):
        self.assertEqual(self.note.title, 'Заголовок новости')
