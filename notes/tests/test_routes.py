from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username="Author")
        cls.notAuthor = User.objects.create(username="notAuthor")
        cls.note = Note.objects.create(
            title="Тестовый заголовок",
            text="Тестовый текст",
            slug="TestSlug",
            author=cls.author,
        )

    def test_pages_availability_for_anonymous_client(self):
        """Страницы доступны неавторизованному пользователю"""
        urls = (
            ("notes:home"),
            ("users:login"),
            ("users:signup"),
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_author(self):
        """Страницы доступны авторизованному пользователю"""

        urls = (
            ("notes:add"),
            ("notes:list"),
            ("notes:success"),
            ("users:logout"),
        )
        for name in urls:
            self.client.force_login(self.author)
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_others_authors_notes_for_author(self):
        """Страницы редактирования удаления и просмотра заметки
        недоступны другому пользователю"""

        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.notAuthor, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            urls = (
                ("notes:edit", (self.note.slug,)),
                ("notes:detail", (self.note.slug,)),
                ("notes:delete", (self.note.slug,)),
            )
            for name, args in urls:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=args)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Перенаправление на страницу авторизации"""
        login_url = reverse("users:login")
        urls = (
            ("notes:add", None),
            ("notes:edit", (self.note.slug,)),
            ("notes:detail", (self.note.slug,)),
            ("notes:delete", (self.note.slug,)),
            ("notes:list", None),
            ("notes:success", None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f"{login_url}?next={url}"
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
