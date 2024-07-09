from http import HTTPStatus
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from notes.models import Note
from pytils.translit import slugify


User = get_user_model()

URL_NOTES_ADD = reverse('notes:add')


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.notAuthor = User.objects.create(username='notAuthor')
        cls.authorClient = Client()
        cls.authorClient.force_login(cls.author)
        cls.notAuthorClient = Client()
        cls.notAuthorClient.force_login(cls.notAuthor)
        cls.testNoteData = {
            "title": "new title",
            "text": "new text",
        }
        cls.authorNote = Note.objects.create(
            title='author Title',
            text='author text',
            slug="authorSlug",
            author=cls.author
        )
        cls.notAuthorNote = Note.objects.create(
            title='notAuthor Title',
            text='notAuthor text',
            slug="notAuthorSlug",
            author=cls.notAuthor
        )
        cls.currentNoteCount = Note.objects.count()

    def test_cant_be_similar_slug(self):
        '''Тест: Нельзя создать заметку с одинаковым slugом'''
        data = {
            "title": "new title",
            "text": "new text",
            "slug": "new-title"
        }
        self.authorClient.post(URL_NOTES_ADD, data)
        self.authorClient.post(URL_NOTES_ADD, data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, self.currentNoteCount + 1)

    def test_anonymous_user_cant_create_note(self):
        '''Тест: анонимный пользователь не может создать заметку'''
        self.client.post(URL_NOTES_ADD, self.testNoteData)
        note_count = Note.objects.count()
        self.assertEqual(note_count, self.currentNoteCount)

    def test_user_can_create_note(self):
        '''Тест: авторизованный пользователь может создать заметку'''
        response = self.authorClient.post(URL_NOTES_ADD, self.testNoteData)
        url = reverse("notes:success")
        self.assertRedirects(response, url)
        note_count = Note.objects.count()
        note = Note.objects.last()
        self.assertEqual(note.text, self.testNoteData['text'])
        self.assertEqual(note.title, self.testNoteData['title'])
        self.assertEqual(note_count, self.currentNoteCount + 1)

    def test_if_slug_is_none_slug_maked_by_slugify(self):
        '''Если при создании заметки поле "Slug" не заполнено, то оно
        формируется автоматически с помощью функции "Slugify"'''
        self.authorClient.post(URL_NOTES_ADD, self.testNoteData)
        slugify_data = slugify(self.testNoteData["title"])
        note = Note.objects.last()
        self.assertEqual(note.slug, slugify_data)

    def test_author_can_delete_note(self):
        '''Тест: автор может удалить свою заметку'''
        url = reverse('notes:delete', args=(self.authorNote.slug,))
        self.authorClient.delete(url)
        note_count = Note.objects.count()
        self.assertEqual(note_count, self.currentNoteCount - 1)

    def test_author_can_update_note(self):
        '''Тест: автор может изменить свою заметку'''
        url = reverse('notes:edit', args=(self.authorNote.slug,))
        data = {
            "title": "updated title",
            "text": "updated text",
        }
        self.authorClient.post(url, data)
        note = Note.objects.get(pk=self.authorNote.pk)
        self.assertEqual(note.title, data['title'])
        self.assertEqual(note.text, data['text'])


    def test_author_cant_delete_comment_of_another_author(self):
        '''Тест: автор не может удалить комментарий другого автора'''
        url = reverse('notes:delete', args=(self.authorNote.slug,))
        response = self.notAuthorClient.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_count = Note.objects.count()
        self.assertEqual(note_count, self.currentNoteCount)
