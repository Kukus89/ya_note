# from django.test import Client, TestCase
# from http import HTTPStatus
from django.urls import reverse
# from notes.models import Note
# from django.contrib.auth import get_user_model


# User = get_user_model()


# class TestRoutes(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.author = User.objects.create(username='testUser')
#         cls.rndAuthor = User.objects.create(username='rndAuthor')
#         cls.note = Note.objects.create(
#             title='Заголовок новости',
#             text='Тестовый текст',
#             slug="myNote",
#             author=cls.author
#         )

#     def test_pages_availability(self):
#         urls = (
#             ('notes:home', None),
#         )
#         for name, args in urls:
#             with self.subTest(name=name):
#                 url = reverse(name, args=args)
#                 response = self.client.get(url)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_availability_for_author(self):
#         users_statuses = (
#             (self.author, HTTPStatus.OK),
#             (self.rndAuthor, HTTPStatus.NOT_FOUND),
#         )
#         for user, status in users_statuses:
#             self.client.force_login(user)
#             urls = (
#                 # ('notes:add', None),
#                 ('notes:edit', (self.note.slug,)),
#                 ('notes:detail', (self.note.slug,)),
#                 ('notes:delete', (self.note.slug,)),
#                 # ('notes:list', None),
#                 # ('notes:success', None),
#             )
#             for name, args in urls:
#                 with self.subTest(user=user, name=name):
#                     url = reverse(name, args=args)
#                     response = self.client.get(url)
#                     self.assertEqual(response.status_code, status)

#     def test_redirect_for_anonymous_client(self):
#         login_url = reverse('users:login')
#         urls = (
#             ('notes:add', None),
#             ('notes:edit', (self.note.slug,)),
#             ('notes:detail', (self.note.slug,)),
#             ('notes:delete', (self.note.slug,)),
#             ('notes:list', None),
#             ('notes:success', None),
#         )
#         for name, args in urls:
#             with self.subTest(name=name):
#                 url = reverse(name, args=args)
#                 redirect_url = f'{login_url}?next={url}'
#                 response = self.client.get(url)
#                 self.assertRedirects(response, redirect_url)


def test_with_client(client):
    response = client.get('/')
    assert response.status_code == 200


def test_closed_page(admin_client):
    url = reverse('notes:list')
    response = admin_client.get(url)
    assert response.status_code == 200
