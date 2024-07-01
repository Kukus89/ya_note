from django.test import Client, TestCase
from notes.models import Note
from django.contrib.auth import get_user_model

# user = get_user_model()


# class TestNote(TestCase):

#     @ classmethod
#     def setUpTestData(cls):
#         cls.user = user.objects.create(username='testUser')
#         cls.user_client = Client()
#         cls.note = Note.objects.create(
#             title='Заголовок новости',
#             text='Тестовый текст',
#             slug="моя закладочка",
#             author=user.objects.first()
#         )

#     def test_successful_creation(self):
#         note_count = Note.objects.count()
#         self.assertEqual(note_count, 1)

#     def test_title(self):
#         self.assertEqual(self.note.title, 'Заголовок новости')
