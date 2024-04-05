from django.contrib.auth import get_user_model
from notes.forms import NoteForm

from .common import BaseTest

User = get_user_model()


class TestContent(BaseTest):

    def test_note_in_list_for_author(self):
        response = self.author_client.get(self.urls['list'])
        object_list = response.context['object_list']
        self.assertIn(self.notes, object_list)

    def test_note_not_in_list_for_another_user(self):
        response = self.reader_client.get(self.urls['list'])
        object_list = response.context['object_list']
        self.assertNotIn(self.notes, object_list)

    def test_pages_contains_form(self):
        urls = ('add', 'edit')
        for name in urls:
            with self.subTest(name=name):
                response = self.author_client.get(self.urls[name])
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
