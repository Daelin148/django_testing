from http import HTTPStatus

from django.contrib.auth import get_user_model

from .common import BaseTest

User = get_user_model()


class TestRoutes(BaseTest):

    def test_pages_availability_for_anonymous_user(self):
        urls = (
            'home',
            'login',
            'logout',
            'signup'
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.client.get(self.urls[name])
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_notes_actions(self):
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            for name in ('detail', 'delete', 'edit'):
                with self.subTest(user=user, name=name):
                    response = user.get(self.urls[name])
                    self.assertEqual(response.status_code, status)

    def test_pages_availability_for_auth_user(self):
        urls = ('list', 'add', 'success')
        for name in urls:
            with self.subTest(name=name):
                response = self.author_client.get(self.urls[name])
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        login_url = self.urls['login']
        for name in (
            'detail',
            'edit',
            'delete',
            'add',
            'success',
            'list',
        ):
            with self.subTest(name=name):
                redirect_url = f'{login_url}?next={self.urls[name]}'
                response = self.client.get(self.urls[name])
                self.assertRedirects(response, redirect_url)
