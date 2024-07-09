from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()

URL_NOTE_LIST = reverse("notes:list")


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username="author")
        cls.authorClient = Client()
        cls.authorClient.force_login(cls.author)
        cls.notAuthor = User.objects.create(username="notAuthor")
        cls.notAuthorClient = Client()
        cls.notAuthorClient.force_login(cls.notAuthor)
        cls.note = Note.objects.create(
            title="author Title",
            text="author text",
            slug="authorSlug",
            author=cls.author,
        )
        cls.noteNotAuthor = Note.objects.create(
            title="not author Title",
            text="not author text",
            slug="notAuthorSlug",
            author=cls.notAuthor,
        )

    def test_note_in_context(self):
        """Тест: заметка пользователя передается со списком заметок
        в словаре 'context'"""
        response = self.authorClient.get(URL_NOTE_LIST)
        object_list = response.context["object_list"]
        Note.objects.create(
            title="author Title",
            text="author text",
            slug="authorSlugNew",
            author=self.author,
        )
        response = self.authorClient.get(URL_NOTE_LIST)
        current_object_list = response.context["object_list"]
        self.assertEqual(current_object_list.count(), object_list.count() + 1)

    def test_author_notes_and_not_author_notes_not_mix(self):
        """Тест: заметки автора и неавтора не пересекаются
        на странице списка заметок"""
        response = self.authorClient.get(URL_NOTE_LIST)
        object_list_author = response.context["object_list"]
        response = self.notAuthorClient.get(URL_NOTE_LIST)
        object_list_notAuthor = response.context["object_list"]
        self.assertNotIn(object_list_author, object_list_notAuthor)

    def test_authorized_client_has_form(self):
        """Тест передачи формы на страницы
        редактирования и создания заметки"""
        urls = (
            ("notes:add", None),
            ("notes:edit", (self.note.slug,)),
        )
        for name, args in urls:
            url = reverse(name, args=args)
            response = self.authorClient.get(url)
            self.assertIn("form", response.context)
            self.assertIsInstance(response.context["form"], NoteForm)
