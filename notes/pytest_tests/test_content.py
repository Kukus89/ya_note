from django.contrib.auth import get_user_model
from django.urls import reverse
import pytest
from notes.forms import NoteForm
User = get_user_model()


@pytest.mark.parametrize(
    'parametrized_client, note_in_list',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('not_author_client'), False),
    )
)
def test_notes_list_for_different_users(
        note, parametrized_client, note_in_list
):
    url = reverse('notes:list')
    response = parametrized_client.get(url)
    assert (note in response.context['object_list']) is note_in_list


@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:add', None),
        ('notes:edit', pytest.lazy_fixture('note_slug'))
    )
)
def test_pages_contained_form(
        name, args, author_client
):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert "form" in response.context
    assert isinstance(response.context['form'], NoteForm)


# class TestContent(TestCase):
#     HOME_URL = reverse('notes:list')

#     @classmethod
#     def setUpTestData(cls):
#         cls.author = User.objects.create(username='testUser')
#         Note.objects.bulk_create(Note(
#             title='Заголовок новости',
#             text='Тестовый текст',
#             slug=f"myNote{index}",
#             author=cls.author) for index in range(11)
#         )

#     def test_notes_count(self):
#         self.client.force_login(self.author)
#         response = self.client.get(self.HOME_URL)
#         object_list = response.context['object_list']
#         notes_count = object_list.count()
#         self.assertEqual(notes_count, 11)

#     def test_anonymous_client_has_no_form(self):
#         url = reverse("notes:home")
#         response = self.client.get(url)
#         self.assertNotIn('form', response.context)

#     def test_authorized_client_has_form(self):
#         self.client.force_login(self.author)
#         url = reverse("notes:add")
#         response = self.client.get(url)
#         self.assertIn('form', response.context)
#         self.assertIsInstance(response.context['form'], NoteForm)
