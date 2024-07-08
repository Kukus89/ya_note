from http import HTTPStatus
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.notAuthor = User.objects.create(username='notAuthor')
        cls.notess = Note.objects.bulk_create(
            Note(
                title='author Title',
                text='author text',
                slug=f"authorSlug{index}",
                author=cls.author
            ) for index in range(10)
        )
        cls.note = Note.objects.create(
            title='author Title',
            text='author text',
            slug="authorSlug",
            author=cls.author
        )
        cls.notesNotAuthor = Note.objects.bulk_create(
            Note(
                title='not author Title',
                text='not author text',
                slug=f"notAuthorSlug{index}",
                author=cls.notAuthor
            ) for index in range(9)
        )

    def test_notes_list(self):
        url = reverse('notes:list')
        self.client.force_login(self.author)
        response = self.client.get(url)
        object_list_author = response.context['object_list']
        self.client.force_login(self.notAuthor)
        response = self.client.get(url)
        object_list_notAuthor = response.context['object_list']
        self.assertNotIn(object_list_author, object_list_notAuthor)

    def test_authorized_client_has_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        self.client.force_login(self.author)
        for name, args in urls:
            url = reverse(name, args=args)
            response = self.client.get(url)
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)
