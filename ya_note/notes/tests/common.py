from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class BaseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }
        cls.author = User.objects.create(username='Лев Толстой')
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )
        cls.reader = User.objects.create(username='Читатель Простой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.urls = {
            'home': reverse('notes:home'),
            'login': reverse('users:login'),
            'logout': reverse('users:logout'),
            'signup': reverse('users:signup'),
            'detail': reverse('notes:detail', args=(cls.notes.slug,)),
            'delete': reverse('notes:delete', args=(cls.notes.slug,)),
            'edit': reverse('notes:edit', args=(cls.notes.slug,)),
            'add': reverse('notes:add'),
            'success': reverse('notes:success'),
            'list': reverse('notes:list'),
        }
