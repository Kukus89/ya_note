import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    "name",
    ("notes:home", "users:login", "users:logout", "users:signup")
)
def test_home_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('notes:list', 'notes:add', 'notes:success')
)
def test_pages_availability_for_auth_user(not_author_client, name):
    url = reverse(name)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('notes:detail', 'notes:edit', 'notes:delete')
)
def test_pages_availability_for_users(
        parametrized_client,
        expected_status,
        name,
        note
):
    url = reverse(name, args=(note.slug,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:detail', pytest.lazy_fixture("note_slug")),
        ('notes:edit', pytest.lazy_fixture("note_slug")),
        ('notes:delete', pytest.lazy_fixture("note_slug")),
        ('notes:add', None),
        ('notes:success', None),
        ('notes:list', None),
    ),
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=(args))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


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
