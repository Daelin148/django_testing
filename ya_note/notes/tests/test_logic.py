# test_logic.py
from http import HTTPStatus

from django.contrib.auth import get_user_model
from notes.forms import WARNING
from notes.models import Note
from pytils.translit import slugify

from .common import BaseTest

User = get_user_model()


class TestNoteCreation(BaseTest):

    def test_user_can_create_note(self):
        response = self.author_client.post(
            self.urls['add'], data=self.form_data
        )
        self.assertRedirects(response, self.urls['success'])
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.get(pk=2)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        response = self.client.post(
            self.urls['add'], data=self.form_data
        )
        expected_url = f'{self.urls["login"]}?next={self.urls["add"]}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), 1)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        response = self.author_client.post(
            self.urls['add'], data=self.form_data
        )
        self.assertRedirects(response, self.urls['success'])
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.get(pk=2)
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.notes.slug
        response = self.author_client.post(
            self.urls['add'], data=self.form_data
        )
        self.assertFormError(
            response, 'form', 'slug',
            errors=(self.notes.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)


class TestNoteEditDelete(BaseTest):

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.urls['edit'], self.form_data)
        self.assertRedirects(response, self.urls['success'])
        edited_note = Note.objects.get(id=self.notes.id)
        self.assertEqual(edited_note.title, self.form_data['title'])
        self.assertEqual(edited_note.text, self.form_data['text'])
        self.assertEqual(edited_note.slug, self.form_data['slug'])

    def test_other_user_cant_edit_note(self):
        response = self.reader_client.post(self.urls['edit'], self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.notes.id)
        self.assertEqual(self.notes.title, note_from_db.title)
        self.assertEqual(self.notes.text, note_from_db.text)
        self.assertEqual(self.notes.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        response = self.author_client.post(self.urls['delete'])
        self.assertRedirects(response, self.urls['success'])
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        response = self.reader_client.post(self.urls['delete'])
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
