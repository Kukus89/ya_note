# import pytest
# from django.test.client import Client
# from notes.models import Note


# @pytest.fixture
# def author(django_user_model):
#     """Фикстура возвращает экземпляр модели автора заметки."""
#     return django_user_model.objects.create(username="Author")


# @pytest.fixture
# def not_author(django_user_model):
#     """Фикстура возвращает экземпляр модели случайного пользователя заметки."""
#     return django_user_model.objects.create(username="not_Author")


# @pytest.fixture
# def author_client(author):
#     """Фикстура возвращает экземпляр клиента с авторизованным пользователем."""
#     client = Client()
#     client.force_login(author)
#     return client


# @pytest.fixture
# def not_author_client(not_author):
#     """Фикстура возвращает экземпляр клиента случайного пользователем."""
#     client = Client()
#     client.force_login(not_author)
#     return client


# @pytest.fixture
# def note(author):
#     """Фикстура возвращает экземпляр заметки с автором."""
#     return Note.objects.create(title="Test note",
#                                text="Test text",
#                                author=author)


# @pytest.fixture
# def note_slug(note):
#     """Фикстура возвращает слаги заметки."""
#     return (note.slug,)


# @pytest.fixture
# def form_data():
#     return {
#         'title': 'Новый заголовок',
#         'text': 'Новый текст',
#         'slug': 'new-slug'
#     }
